#!/bin/bash
set -e

cd src/piper/tests/
pytest

cd data/blueprint/complex
piper blueprint --local-blueprints ../locals
cd ../../

cd complexproject
piper clean
piper setup
cd microservices/second/
venv-second/bin/python -m second

piper pack sdist

piper clean

piper pack --no-setup sdist
( venv-second/bin/python -m second && exit 1 ) || echo No setup ok
piper clean
