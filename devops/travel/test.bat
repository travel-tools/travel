@echo off


cd src\travel\tests\
pytest

cd data\plan\complex
travel plan test
travel add gh:travel-tools/cookiecutter-travelplan --no-input
cd ..\..\

cd complexproject
travel clean
travel setup
cd microservices\second
venv-second\Scripts\python -m second

travel pack sdist

travel clean

travel pack --no-setup sdist
( venv-second\Scripts\python -m second && exit 1 ) || echo No setup ok
venv-second\Scripts\python -m pip install build\package\dist\second-0.0.0.tar.gz
venv-second\Scripts\python -m second
travel clean
