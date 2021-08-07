import logging
import os
import re
import subprocess

from piper.config.pipe import Pipe
from piper.tools.pip import Pip
from piper.tools.python import Python
from piper.tools.shell import Shell

logger = logging.getLogger(__name__)


_CREATE_VENV = "(" + ") || (".join(["{python} -m venv {venv}",
                                    "virtualenv -p {python} {venv}",
                                    "pip install virtualenv && virtualenv -p {python} {venv}"]) + ")"


class Virtualenv:

    def __init__(self, main_python: Python, pipe: Pipe):
        self._main_python = main_python
        self._name = f"venv-{pipe.name}"

        self.pipe = pipe
        self.path = os.path.join(pipe.location, self._name)
        activate = _get_activate_command(self.path)
        self.python = Python(path=os.path.join(self.path, "bin" if os.name == "posix" else "Scripts", "python" if os.name == "posix" else "python.exe"), pre_command=activate)
        self.pip = Pip(pre_command=activate)

    def create(self) -> None:
        # Create the virtualenv if it does not exist
        if os.path.exists(self.path):
            logger.info(f"Virtualenv already exists for {self._name}")
        else:
            # Create the virtualenv with the template command
            logger.info(f"Creating the virtual environment for {self._name}...")
            Shell().run(
                _CREATE_VENV.format(
                    python=self._main_python.path,
                    venv=self.path
                )
            )

    def update(self):

        # Install requirements
        logger.info("Installing requirements...")
        for pipe in [*self.pipe.flat_dependencies(), self.pipe]:
            out = self.pip.run(f"install -e {pipe.setup_py_folder}")
            logger.info(f"{out.stdout}, {out.stderr}")
            if pipe.requirements:
                out = self.pip.run(f"install {' '.join([f'{name}=={version}' for name, version in pipe.requirements.items()])}")
                logger.info(f"{out.stdout}, {out.stderr}")
        logger.info("Done.")

    def freeze(self):

        # Pip freeze
        output = self.pip.run(f"freeze").stdout
        requirements = re.sub("[\r\n]+", "\n", output).split("\n")

        # Get real requirements and update the requirements.txt file
        real_requirements = [req for req in requirements if _is_valid_requirement(req)]
        with open(self.pipe.requirements_file, "w") as f:
            for requirement in real_requirements:
                f.write(requirement + "\n")
            logger.info(f"Freezing {real_requirements}")


def _is_valid_requirement(requirement: str) -> bool:

    # List of requirements to filter out
    forbidden_requirements = [
        "pkg-resources",
        "^-e",
        "^#",
        "pywin32",
        "pywinpty"
    ]
    forbidden_match = "(" + ")|(".join(forbidden_requirements) + ")"

    # Check if there is one match
    return requirement and not re.match(forbidden_match, requirement)


def _get_activate_command(path) -> str:
    # Get activate command
    if os.name == "nt":
        activate = f"{path}\\Scripts\\activate"
    elif os.name == "posix":
        activate = f". {path}/bin/activate"
    else:
        raise NotImplementedError(f"Operating System {os.name} not supported.")
    return activate
