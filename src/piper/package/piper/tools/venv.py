import logging
import os
import re
import subprocess
from typing import List

from piper.config.pipe import Pipe
from piper.config.sanitizers import pip_sanitizer
from piper.tools.pip import Pip
from piper.tools.python import Python
from piper.tools.python import main_python as default_python
from piper.tools.shell import Shell

logger = logging.getLogger(__name__)


_CREATE_VENV = "{python} -m venv {venv}"


class Virtualenv:

    def __init__(self, pipe: Pipe, main_python: Python = default_python):
        self._main_python = main_python
        self._name = f"venv-{pipe.name}"

        self.pipe = pipe
        self.path = os.path.join(pipe.location, self._name)
        self.python = Python(path=os.path.join(self.path, "bin" if os.name == "posix" else "Scripts", "python" if os.name == "posix" else "python.exe"))
        self.pip = Pip(self.python)

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
        explicit_requirements = []
        for pipe in self.pipe.flat_dependencies(with_current=True):

            # Install the pipe's package
            self.pip.run(f"install -e {pipe.setup_py_folder}")

            # Install the explicit requirements
            if pipe.requirements:
                self.pip.install(pipe.requirements)
                explicit_requirements = explicit_requirements + pipe.requirements

        # Uninstall the unnecessary requirements
        installed_requirements = [pip_sanitizer.get_package_name(f) for f in self._freeze()]
        necessary_requirements = self._recursive_requirements(explicit_requirements) if explicit_requirements else []
        unnecessary_requirements = set(installed_requirements) - set(necessary_requirements)
        if unnecessary_requirements:
            to_uninstall = ' '.join(list(unnecessary_requirements))
            logger.warning(f"Unnecessary requirements found, they will be uninstalled: {to_uninstall}")
            self.pip.run(f"uninstall -y {to_uninstall}")

        logger.info("Done.")

    def _freeze(self) -> List[str]:

        try:

            # Pip freeze
            output = self.pip.run(f"freeze", capture=True).stdout
            requirements = re.sub("[\r\n]+", "\n", output).split("\n")

            # Get real requirements
            return [req for req in requirements if _is_valid_requirement(req)]

        except subprocess.CalledProcessError as e:
            logger.error(e.stderr)
            exit(e.returncode)

    def freeze(self):

        # Update requirements file
        real_requirements = self._freeze()
        with open(self.pipe.requirements_file, "w") as f:
            for requirement in real_requirements:
                f.write(requirement + "\n")
            logger.info(f"Freezing {real_requirements}")

    def _recursive_requirements(self, requirements: List[str]) -> List[str]:

        def _find_recursively(reqs):

            # Parse this level requirements
            explicit_requirements = [pip_sanitizer.get_package_name(req) for req in reqs]

            # Get the implicit requirements, needed by these requirements
            output = self.pip.run(f"show {' '.join(explicit_requirements)}", capture=True).stdout
            implicit = [
                req
                for line in re.sub("[\r\n]+", "\n", output).split("\n") if line.startswith("Requires: ")
                for req in line.replace("Requires: ", "").split(", ") if req
            ]

            # If any implicit, recursively get their implicit ones; else return it simply
            if implicit:
                requires = explicit_requirements + _find_recursively(implicit)
            else:
                requires = explicit_requirements
            return requires

        return list(set(_find_recursively(requirements)))


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
