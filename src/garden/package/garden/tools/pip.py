from typing import List, Union

from garden.config.reader import read_all_nests
from garden.config.sanitizers.pip_sanitizer import sanitize_package, sanitize_versioned_package, is_just_package
from garden.tools.executable import Executable
from garden.tools.python import Python


class Pip(Executable):

    def __init__(self, python: Python, pre_command: str = None):
        super().__init__(f"{python.path} -m pip --disable-pip-version-check", pre_command=pre_command)

    def install(self, requirements: Union[List[str], str], allow_nests_from: Union[str, List[str]] = None):

        if isinstance(requirements, str):
            requirements = [requirements]

        # Install real requirements
        packages = [
            f'{sanitize_versioned_package(req)}'
            for req in requirements
            if not is_just_package(req)
        ]
        if packages:
            super().run(f"install {' '.join(packages)}")

        # Install nests
        nests = [
            f'{sanitize_package(req)}'
            for req in requirements
            if is_just_package(req)
        ]
        if nests:
            if not allow_nests_from:
                raise ValueError(f"{nests} without versions (or nests) are not allowed here")
            else:
                allow_nests_from = allow_nests_from if isinstance(allow_nests_from, list) else [allow_nests_from]
                for context in allow_nests_from:
                    all_nests = read_all_nests(context)
                    super().run(f"install -e {' '.join([n.setup_py_folder for n in all_nests.values() if n.name in nests])}")
