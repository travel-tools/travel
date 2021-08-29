@echo off


cd src\piper\tests\
pytest

cd data\complexproject
piper setup
cd microservices\second
venv-second\Scripts\python package\second\__init__.py

piper pack sdist

piper clean
