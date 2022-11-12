@echo off


cd src\travel\tests\
pytest

cd data\plan\complex
travel --debug plan test
travel --debug add gh:travel-tools/cookiecutter-travelplan --no-input
cd ..\..\

cd complexproject
travel --debug clean

:: Python version
:: no compatible python
echo python: 2.7.1 > bag.yml
( travel setup && exit 1 ) || echo No python ok

:: wrong config (2.7.1 pointing to python 3)
for /F "tokens=*" %%p IN ('python -c "import sys; print(sys.executable)"') DO @(travel config add python 2.7.1 %%p)
( travel setup && exit 1 ) || echo Wrong python version ok

:: right config
python -c "import sys; print('python: ' + sys.version.split(' ')[0])" > bag.yml
for /F "tokens=*" %%p IN ('python -c "import sys; print(sys.version.split()[0], sys.executable)"') DO @(travel config add python %%p)
travel --debug setup
:: End Python version

cd microservices\second
venv-second\Scripts\python -m second

travel --debug pack sdist

travel --debug clean

travel --debug pack --no-setup sdist
( venv-second\Scripts\python -m second && exit 1 ) || echo No setup ok
python -m pip install build\package\dist\second-0.0.0.tar.gz
python -m second
travel --debug clean
