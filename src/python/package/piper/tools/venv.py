import logging
import os
import subprocess

from piper.tools.python import Python

logger = logging.getLogger(__name__)

_CREATE_VENV = "(" + ") || (".join(["{python} -m venv {venv}",
                                    "virtualenv -p {python} {venv}",
                                    "pip install virtualenv && virtualenv -p {python} {venv}"]) + ")"


class Virtualenv:

    def __init__(self, main_python: Python, location: str, name: str):
        self._main_python = main_python
        self._location = location
        self._name = name
        self._path = os.path.join(location, name)

    def create(self) -> None:
        # Create the virtualenv if it does not exist
        if os.path.exists(self._path):
            logger.info("Virtualenv already exists")
        else:
            # Create the virtualenv with the template command
            logger.info("Creating the virtual environment...")
            subprocess.run(
                _CREATE_VENV.format(
                    python=self._main_python.path,
                    venv=self._path
                ),
                check=True,
                shell=True
            )
    
    def get_python(self) -> Python:
        # TODO
        pass

    def update(self):

        # Install requirements
        print("Installing requirements...")
        activate_command = self._get_venv_activate_command()
        subprocess.run(VENV_UPDATE.format(activate_command=activate_command), check=True, shell=True)
        print("Done.")