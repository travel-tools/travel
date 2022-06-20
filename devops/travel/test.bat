@echo off


cd src\travel\tests\
pytest

cd data\plan\complex
travel --debug plan test
travel --debug add gh:travel-tools/cookiecutter-travelplan --no-input
cd ..\..\

cd complexproject
travel --debug clean
travel --debug setup
cd microservices\second
venv-second\Scripts\python -m second

travel --debug pack sdist

travel --debug clean

travel --debug pack --no-setup sdist
( venv-second\Scripts\python -m second && exit 1 ) || echo No setup ok
python -m pip install build\package\dist\second-0.0.0.tar.gz
python -m second
travel --debug clean
