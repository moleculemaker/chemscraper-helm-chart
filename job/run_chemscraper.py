#!/usr/bin/env python3
import csv
import gc
import logging
import os
import pandas as pd
import re
import zipfile
from pathlib import Path
from urllib.error import HTTPError

import sys
import traceback
from io import BytesIO, StringIO

from models import Molecule
from services import PubChemService, RDKitService
from chemscraper.fast_api_client import Client
from chemscraper.fast_api_client.types import File
from chemscraper.fast_api_client.api.default import extract_extract_pdf_post as extract_pdf_post
from chemscraper.fast_api_client.api.default.extract_extract_pdf_post import BodyExtractExtractPdfPost as BodyExtractPdfPost

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logger = logging.getLogger('run_chemscraper')
logger.setLevel(LOG_LEVEL)

# Path to input PDFs for RM+CS
# Files in this path will be automatically downloaded from MinIO before running the AlphaSynthesis job
CHEMSCRAPER_INPUT_FILE = os.getenv('CHEMSCRAPER_INPUT_FILE', '/usr/app/inputs/or100.09.tables.small.pdf')

# Path to output from full RM+CS workflow
# We store to the same path as ReactionMiner outputs, so that this is also uploaded to MinIO
CHEMSCRAPER_OUTPUT_DIR = os.getenv('CHEMSCRAPER_OUTPUT_DIR', '/usr/app/outputs')

# Base URL to ChemScraper API
# We will override this default in production
CHEMSCRAPER_BASE_URL = os.getenv('CHEMSCRAPER_BASE_URL', 'http://chemscraper-services-staging.staging.svc.cluster.local:8000')

# Unique identifier for each job
JOB_ID = os.getenv('JOB_ID')


# Shared services that we borrowed from mmli-backend
pubChemService = PubChemService()
rdkitService = RDKitService()


# Submit input PDF file to Chemscraper API
def submit_to_chemscraper(pdf_file):
    # Create a new ChemScraper API client and submit the
    # PDF + JSON files and the mapping that links them
    with Client(base_url=CHEMSCRAPER_BASE_URL) as client:
        return extract_pdf_post.sync(
            client=client,
            generate_svg=True,
            body=BodyExtractPdfPost(
                pdf=File(
                    file_name=pdf_file.split(os.path.sep)[-1],
                    payload=read_file_bytes(pdf_file),
                    mime_type='application/pdf'
                )
            )
        )


# Returns file contents as bytes
def read_file_bytes(path: str) -> BytesIO:
    with open(path, mode='rb') as f:
        return BytesIO(f.read())


# Write ChemScraper response to file
def write_output_files(output_path: str, response):
    # Extract response zip to output diretory
    logger.info(f'Writing response files: {output_path}')
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    zip_file.extractall(CHEMSCRAPER_OUTPUT_DIR)

    # Locate and parse TSV file contents
    file_list = zip_file.namelist()
    tsv_file_name = next((file for file in file_list if file.endswith('.tsv')), None)
    tsv_file_path = os.path.join(CHEMSCRAPER_OUTPUT_DIR, tsv_file_name)
    tsv_file_contents = read_file_bytes(tsv_file_path)

    # Write output CSV
    write_results_csv(tsv_file_contents.getvalue())


def write_results_csv(tsv_content: bytes):
    reader = csv.reader(tsv_content.decode().splitlines(), delimiter='\t')
    doc_no = file_path = page_no = SMILE = minX = minY = maxX = maxY = SVG = None
    molecules = []
    id = 0
    otherInstancesDict = {}
    SMILE_LIST = []

    for row in reader:
        if not row:
            continue
        if row[0] == "D":
            # Format: D	1	/inputs/tmp_inpdfs/or100.09.tables.pdf detected=243 parsed=243 converted=243 version=0.4.3
            doc_no, full_metadata = row[1], row[2]

            # Parse full metadata into file_path, version, and stat counters
            pattern = r"(?P<file_path>.+) detected=(?P<num_detected>.+) parsed=(?P<num_parsed>.+) converted=(?P<num_converted>.+) version=(?P<version>.+)"
            match = re.match(pattern, row[2])
            if match:
                file_path = match.group('file_path')

                # TODO: the version + stat counters are currently unused
                #num_detected = match.group('num_detected')
                #num_parsed = match.group('num_parsed')
                #num_converted = match.group('num_converted')
                #version = match.group('version')

        if row[0] == "P":
            # Format: P	1	1000	1000
            page_no = row[1]

        # Ignored for now?
        if row[0] == "FR":
            # Format: FR	2	825	1950	1020	2056
            continue

        if row[0] == "SMI":
            # Format: SMI	1	COC(=O)C*	1609	1949	1810	2057
            SMILE = row[2]
            minX, minY, maxX, maxY = map(int, row[3:7])
            if all([doc_no, file_path, page_no, SMILE, minX, minY, maxX, maxY]):
                # Only molecules having all these fields available are processed
                SMILE_LIST.append(SMILE)
                svg_filename = f"Page_{page_no.zfill(3)}_No{row[1].zfill(3)}.svg"
                logger.debug(f'Processing row:   doc_no={doc_no}   file_path={file_path}   page_no={page_no}   SMILE={SMILE}    X={minX}:{maxX}    Y={minY}:{maxY}')
                pdf_stem = Path(file_path).stem
                #logger.debug(f'Using file stem: {pdf_stem}')
                svg_path = f'{CHEMSCRAPER_OUTPUT_DIR}/{pdf_stem}/{svg_filename}'

                #logger.debug(f'Attempting to read SVG from ChemScraper output: {svg_path}')
                with open(svg_path, mode='r') as f:
                    SVG = f.read()
                if SVG is None:
                    logger.warning("SVG not found, generating using rdkit")
                    SVG = rdkitService.renderSVGFromSMILE(smileString=SMILE)

                location = " | page: " + page_no

                if SMILE in otherInstancesDict:
                    otherInstancesDict[SMILE].append(page_no)
                else:
                    otherInstancesDict[SMILE] = [page_no]
                try:
                    fingerprint = rdkitService.getFingerprint(SMILE)
                except Exception as e:
                    logger.error("Could not generate fingerprint for: " + SMILE)
                    fingerprint = "0"
                try:
                    atom_count = rdkitService.getAtomCount(SMILE)
                except Exception as e:
                    logger.error("Could not generate atom count for: " + SMILE)
                    atom_count = 0
                molecules.append(
                    Molecule(
                        id=id,
                        flagged=False,
                        atom_count=atom_count,
                        doc_no=doc_no,
                        file_path=file_path,
                        page_no=page_no,
                        SMILE=SMILE, 
                        structure=SVG, 
                        minX=minX, 
                        minY=minY, 
                        width=maxX-minX, 
                        height=maxY-minY,
                        Location=location,
                        OtherInstances=[],
                        fingerprint=fingerprint
                    )
                )
                id += 1

    # Only for debugging
    # TODO: Remove after Pub Chem Batching tested in PROD
    logger.debug('=== Printing Smile List ====')
    logger.debug(SMILE_LIST)
    logger.debug('=== End Printing Smile List ====')

    # Get data for all molecules
    molecules_data = pubChemService.getDataForAllMolecules(SMILE_LIST)

    # Only for debugging
    # TODO: Remove after Pub Chem Batching tested in PROD
    logger.debug('======== Printing All Molecule Data =======')
    data_idx = 0

    # Short-circuit if no PubChem molecule information is found
    if molecules_data is None:
        logger.warning(f'No PubChem molecule results found - skipping: {molecules_data}')
        return

    while data_idx < len(molecules_data):
        logger.debug(f'{molecules_data[data_idx]} {molecules_data[data_idx+1]} {molecules_data[data_idx+2]} {molecules_data[data_idx+3]} {molecules_data[data_idx+4]}')
        data_idx += 5
    logger.debug('======== End Printing All Molecule Data ======')

    # To iterate Molecule Data Array - molecules_data
    molecules_data_idx = 0

    # Setting Pubchem results directly to CSV
    data = [m.dict() for m in molecules]
    for d in data:
        d['chemicalSafety'] = ', '.join(d['chemicalSafety'])
        d['OtherInstances'] = ', '.join(otherInstancesDict.get(d['SMILE'], []))
        d['PubChemCID'] = molecules_data[molecules_data_idx + 1]
        d['molecularFormula'] = molecules_data[molecules_data_idx + 2]
        d['molecularWeight'] = molecules_data[molecules_data_idx + 3]
        d['name'] = molecules_data[molecules_data_idx + 4]
        molecules_data_idx += 5

    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    csv_data = csv_buffer.getvalue().encode('utf-8')

    # Write result CSV file
    output_path = f"/{CHEMSCRAPER_OUTPUT_DIR}/{JOB_ID}-results.csv"
    with open(output_path, "wb") as f:
        logger.info(f"Writing CSV result file contents: {output_path}")
        f.write(csv_data)

    return


# Walk directory and build up a mapping to submit to ChemScraper
# exit with error code = 1 if any error encountered
# (error code = 0 indicates success)
if __name__ == "__main__":
    logger.info(f'Submitting these files to ChemScraper')
    logger.info(f'        Input Dir:  {CHEMSCRAPER_INPUT_FILE}')
    logger.info(f'       Output Dir:  {CHEMSCRAPER_OUTPUT_DIR}')
    logger.info(f'  ChemScraper URL:  {CHEMSCRAPER_BASE_URL}')

    try:
        logger.info(f'Submitting PDF file to ChemScraper...')
        resp = submit_to_chemscraper(pdf_file=CHEMSCRAPER_INPUT_FILE)

        # Raise error status if no response body
        #logger.debug("Response: " + str(resp))

        # Write response to file
        if resp is not None:
            # Convert response dictionary to JSON
            write_output_files(output_path=CHEMSCRAPER_OUTPUT_DIR, response=resp)
            logger.info('Job completed successfully!')
        else:
            # Handle response errors
            logger.error('Error submitting to ChemScraper - empty response encountered')
            sys.exit(1)

    except Exception as ex:
        logger.error(f'ERROR: {ex}')
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        logger.warning(f'Cleaning up resources...')
        collected_count = gc.collect()
        logger.warning(f'Cleaned up resources: {collected_count}')
