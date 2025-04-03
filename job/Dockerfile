#FROM python:3-slim
FROM mambaorg/micromamba:2
WORKDIR /usr/app/

# Install Dependencies
#COPY requirements.txt ./
#RUN pip install -r requirements.txt --no-cache-dir

COPY environment.yml ./
RUN micromamba env update -n base -f environment.yml
SHELL [ "micromamba", "run", "-n", "base" ]

# Generate ChemScraper API Client
#COPY generate-client.sh ./
#RUN ./generate-client.sh

# Entrypoint script
COPY run_chemscraper.py ./
CMD [ "python", "./run_chemscraper.py" ]
