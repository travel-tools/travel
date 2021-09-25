from typing import List, Union

from piper.config.reader import read_all_pipes
from piper.config.sanitizers.pip_sanitizer import sanitize_package, sanitize_versioned_package, is_just_package
from piper.tools.executable import Executable
from piper.tools.python import Python


class Pip(Executable):

    def __init__(self, python: Python, pre_command: str = None):
        super().__init__(f"{python.path} -m pip --disable-pip-version-check", pre_command=pre_command)

    def install(self, requirements: Union[List[str], str], allow_pipes_from: Union[str, List[str]] = None):

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

        # Install pipes
        pipes = [
            f'{sanitize_package(req)}'
            for req in requirements
            if is_just_package(req)
        ]
        if pipes:
            if not allow_pipes_from:
                raise ValueError(f"{pipes} without versions (or pipes) are not allowed here")
            else:
                allow_pipes_from = allow_pipes_from if isinstance(allow_pipes_from, list) else [allow_pipes_from]
                for context in allow_pipes_from:
                    all_pipes = read_all_pipes(context)
                    super().run(f"install -e {' '.join([p.setup_py_folder for p in all_pipes.values() if p.name in pipes])}")
