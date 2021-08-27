@echo off


cd src\piper\tests\data\complexproject
piper setup
cd microservices\second
venv-second\Scripts\python package\second\__init__.py
piper clean
