#!/bin/bash
set -e

cd src/travel/tests/
pytest

cd data/blueprint/complex
travel blueprint --local-blueprints ../locals
cd ../../

cd complexproject
travel clean
travel setup
cd microservices/second/
venv-second/bin/python -m second

travel pack sdist

travel clean

travel pack --no-setup sdist
( venv-second/bin/python -m second && exit 1 ) || echo No setup ok
venv-second/bin/python -m pip install build/package/dist/second-0.0.0.tar.gz
venv-second/bin/python -m second
travel clean
