@echo off


cd src\piper\tests\
pytest

cd data\blueprint\complex
piper blueprint --local-blueprints ..\locals
cd ..\..\

cd complexproject
piper clean
piper setup
cd microservices\second
venv-second\Scripts\python package\second\__init__.py

piper pack sdist

piper clean