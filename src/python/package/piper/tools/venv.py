import logging
import os
import re
import subprocess

from piper.config.pipe import Pipe
from piper.tools.pip import Pip
from piper.tools.python import Python

logger = logging.getLogger(__name__)


_CREATE_VENV = "(" + ") || (".join(["{python} -m venv {venv}",
                                    "virtualenv -p {python} {venv}",
                                    "pip install virtualenv && virtualenv -p {python} {venv}"]) + ")"


class Virtualenv:

    def __init__(self, main_python: Python, pipe: Pipe):
        self._main_python = main_python
        self._name = f"venv-{pipe.name}"
        self._path = os.path.join(pipe.location, self._name)

        self.pipe = pipe
        activate = self._get_activate_command()
        self.python = Python(path=os.path.join(self._path, ""), pre_command=activate)
        self.pip = Pip(pre_command=activate)

    def create(self) -> None:
        # Create the virtualenv if it does not exist
        if os.path.exists(self._path):
            logger.info(f"Virtualenv already exists for {self._name}")
        else:
            # Create the virtualenv with the template command
            logger.info(f"Creating the virtual environment for {self._name}...")
            subprocess.run(
                _CREATE_VENV.format(
                    python=self._main_python.path,
                    venv=self._path
                ),
                check=True,
                shell=True
            )

    def _get_activate_command(self) -> str:
        # Get activate command
        if os.name == "nt":
            activate = f"{self._path}\\Scripts\\activate"
        elif os.name == "posix":
            activate = f"source {self._path}/bin/activate"
        else:
            raise NotImplementedError(f"Operating System {os.name} not supported.")
        return activate

    def update(self):

        # Install requirements
        logger.info("Installing requirements...")
        for pipe in [*self.pipe.flat_dependencies(), self.pipe]:
            self.pip.run(f"install -e {pipe.setup_py_folder}")
            if pipe.requirements:
                self.pip.run(f"install {' '.join([f'{name}=={version}' for name, version in pipe.requirements.items()])}")
        logger.info("Done.")

    def freeze(self):

        # Pip freeze
        output = self.pip.run(f"freeze")
        requirements = re.sub("[\r\n]+", "\n", output).split("\n")

        # Get real requirements and update the requirements.txt file
        real_requirements = [req for req in requirements if is_valid_requirement(req)]
        with open(self.pipe.requirements_file, "w") as f:
            for requirement in real_requirements:
                f.write(requirement + "\n")


def is_valid_requirement(requirement: str) -> bool:

    # List of requirements to filter out
    forbidden_requirements = [
        "pkg-resources",
        "^-e",
        "pywin32",
        "pywinpty"
    ]
    forbidden_match = "(" + ")|(".join(forbidden_requirements) + ")"

    # Check if there is one match
    return not re.match(forbidden_match, requirement)
