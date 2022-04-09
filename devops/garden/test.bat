@echo off


cd src\garden\tests\
pytest

cd data\blueprint\complex
garden blueprint --local-blueprints ..\locals
cd ..\..\

cd complexproject
garden clean
garden setup
cd microservices\second
venv-second\Scripts\python -m second

garden pack sdist

garden clean

garden pack --no-setup sdist
( venv-second\Scripts\python -m second && exit 1 ) || echo No setup ok
venv-second\Scripts\python -m pip install build\package\dist\second-0.0.0.tar.gz
venv-second\Scripts\python -m second
garden clean
