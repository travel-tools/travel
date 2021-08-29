#!/bin/bash
set -e

cd src/piper/tests/
pytest

cd data/complexproject
piper setup
cd microservices/second/
venv-second/bin/python package/second/__init__.py

piper pack sdist

piper clean
