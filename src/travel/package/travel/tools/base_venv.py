import logging
import os
import re
import subprocess
from pathlib import Path
from typing import List

from travel.config.bag import Bag
from travel.config.sanitizers import pip_sanitizer
from travel.config.sanitizers.pip_sanitizer import LATEST_PIP
from travel.config.subconfigs.pip import PipConfig
from travel.tools.outputs.latest_updates import LatestUpdate
from travel.tools.pip import Pip
from travel.tools.python import Python
from travel.tools.python import main_python as default_python
from travel.tools.shell import Shell

logger = logging.getLogger(__name__)


_CREATE_VENV = "{python} -m venv {venv}"
LATEST_UPDATE = "latest_update.yml"


class BaseVirtualenv:

    def __init__(self, location: str, name_suffix: str, pip_config: PipConfig, dependencies: List[Bag], requirements_file: str, main_python: Python = default_python, touch_requirements_file: bool = False, extra_requirements: List[str] = None):
        self._main_python = main_python
        self._name = f"venv-{name_suffix}"

        self.pip_config = pip_config
        self.dependencies = dependencies
        self.requirements_file = requirements_file
        self.extra_requirements = extra_requirements

        self.location = location
        self.path = os.path.join(location, self._name)
        self.python = Python(path=os.path.join(self.path, "bin" if os.name == "posix" else "Scripts", "python" if os.name == "posix" else "python.exe"))
        self.pip = Pip(self.python)

        # Prepare the requirements file
        if touch_requirements_file:
            if not os.path.isfile(requirements_file):
                Path(requirements_file).touch()

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

    def update(self) -> bool:

        # Upgrade pip if required
        pip_version = self.pip_config.version
        if pip_version:
            logger.info("Check pip version...")
            if pip_version == LATEST_PIP:
                self.pip.run("install --upgrade pip")
            else:
                self.pip.install(f"pip=={pip_version}")

        # Compute current requirements
        dependency_names = [bag.name for bag in self.dependencies]
        explicit_requirements = [req for bag in self.dependencies for req in bag.requirements]
        if self.extra_requirements:
            explicit_requirements = explicit_requirements + self.extra_requirements

        # If there is already a requirements file and a latest_update file, check: we might skip the update!
        latest_update_path = Path(self.path)/LATEST_UPDATE
        if Path(self.requirements_file).is_file() and latest_update_path.is_file():

            # Get the freezed requirements and the written requirements
            freezed_requirements = self._freeze()
            with open(self.requirements_file, "r") as f:
                written_requirements = f.read().splitlines()
            
            # Read the latest_update
            latest_update = LatestUpdate.read(latest_update_path)

            # If there is nothing to update, exit!
            if (set(freezed_requirements) == set(written_requirements)
                    and set(dependency_names) == set(latest_update.dependencies)
                    and set(explicit_requirements) == set(latest_update.requirements)):
                logger.info("Virtualenv is already up-to-date!")
                return False

        # Install requirements
        logger.info("Installing requirements...")
        for bag in self.dependencies:
            # Install the bag's package
            self.pip.run(f"install -e {bag.setup_py_folder}")
            # Install the explicit requirements
            if bag.requirements:
                self.pip.install(bag.requirements)

        if self.extra_requirements:
            self.pip.install(self.extra_requirements)

        # Uninstall the unnecessary requirements
        installed_requirements = [pip_sanitizer.get_package_name(f) for f in self._freeze()]
        necessary_requirements = self._recursive_requirements(explicit_requirements) if explicit_requirements else []
        unnecessary_requirements = set(installed_requirements) - set(necessary_requirements)
        if unnecessary_requirements:
            to_uninstall = ' '.join(list(unnecessary_requirements))
            logger.warning(f"Unnecessary requirements found, they will be uninstalled: {to_uninstall}")
            self.pip.run(f"uninstall -y {to_uninstall}")

        # Save the latest update
        LatestUpdate.create(
            requirements=explicit_requirements,
            dependencies=dependency_names
        ).write(latest_update_path)

        logger.info("Done.")
        return True

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
        with open(self.requirements_file, "w") as f:
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
