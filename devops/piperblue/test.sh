#!/bin/bash

# Testing the blueprint
pip install -e src/piperblue/tests/data/piperblueexample/package
python -m pytest --doctest-modules --junitxml=junit/test-results.xml --cov=com --cov-report=xml --cov-report=html
