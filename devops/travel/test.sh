#!/bin/bash
set -e

cd src/travel/tests/
pytest

cd data/plan/complex
travel --debug plan test
travel --debug add gh:travel-tools/cookiecutter-travelplan --no-input
cd ../../

cd complexproject
travel --debug clean

echo "python: 2.7.1" > bag.yml
( travel setup && exit 1 ) || echo Wrong python ok

python -c 'import sys; print("python: " + sys.version.split(" ")[0])' > bag.yml

travel --debug setup
cd microservices/second/
venv-second/bin/python -m second

travel --debug pack sdist

travel --debug clean

travel --debug pack --no-setup sdist
( venv-second/bin/python -m second && exit 1 ) || echo No setup ok
python -m pip install build/package/dist/second-0.0.0.tar.gz
python -m second
travel --debug clean
