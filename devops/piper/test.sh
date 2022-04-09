#!/bin/bash
set -e

cd src/garden/tests/
pytest

cd data/blueprint/complex
garden blueprint --local-blueprints ../locals
cd ../../

cd complexproject
garden clean
garden setup
cd microservices/second/
venv-second/bin/python -m second

garden pack sdist

garden clean

garden pack --no-setup sdist
( venv-second/bin/python -m second && exit 1 ) || echo No setup ok
venv-second/bin/python -m pip install build/package/dist/second-0.0.0.tar.gz
venv-second/bin/python -m second
garden clean
