#!/bin/bash

# Testing the blueprint
pip install -e src/piperblue/tests/data/piperblueexample/package
python -m pytest src/piperblue/tests/src/
