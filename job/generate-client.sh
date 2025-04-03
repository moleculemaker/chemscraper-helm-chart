#!/bin/bash
#openapi-python-client generate --overwrite --url 'https://chemscraper.backend.staging.mmli1.ncsa.illinois.edu/openapi.json' --output-path ./chemscraper/
openapi-python-client generate --overwrite --url 'http://host.docker.internal:8000/openapi.json' --output-path ./chemscraper/
