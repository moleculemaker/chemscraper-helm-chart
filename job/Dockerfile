FROM mambaorg/micromamba:alpine

# FIXME: Temporary workaround for NFS file permissions issues
USER root

WORKDIR /usr/app/

# Use a drop-in for conda executable
ENV CONDA='micromamba'

# Install dependencies using conda
COPY environment.yml .
RUN ${CONDA} env update -n base -f environment.yml && ${CONDA} clean --all 
SHELL [ "${CONDA}", "run", "-n", "base" ]

# Generate ChemScraper API Client
# FIXME: We needed to manually change one line of the generated code
#COPY generate-client.sh .
#RUN ./generate-client.sh

# Supporting Python files
COPY chemscraper ./chemscraper
COPY models ./models
COPY services ./services

# Entrypoint script
COPY run_chemscraper.py .
CMD [ "python", "./run_chemscraper.py" ]
