from typing import List, Union

from travel.config.reader import read_all_bags
from travel.config.sanitizers.pip_sanitizer import sanitize_package, sanitize_versioned_package, is_just_package
from travel.tools.executable import Executable
from travel.tools.python import Python


class Pip(Executable):

    def __init__(self, python: Python, pre_command: str = None):
        super().__init__(f"{python.path} -m pip --disable-pip-version-check", pre_command=pre_command)

    def install(self, requirements: Union[List[str], str], allow_bags_from: Union[str, List[str]] = None):

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

        # Install bags
        bags = [
            f'{sanitize_package(req)}'
            for req in requirements
            if is_just_package(req)
        ]
        if bags:
            if not allow_bags_from:
                raise ValueError(f"{bags} without versions (or bags) are not allowed here")
            else:
                allow_bags_from = allow_bags_from if isinstance(allow_bags_from, list) else [allow_bags_from]
                for context in allow_bags_from:
                    all_bags = read_all_bags(context)
                    super().run(f"install -e {' '.join([b.setup_py_folder for b in all_bags.values() if b.name in bags])}")
