from typing import List, Union

from piper.config.reader import read_all_pipes
from piper.config.sanitizers.pip_sanitizer import sanitize_package, sanitize_versioned_package, is_just_package
from piper.tools.executable import Executable


class Pip(Executable):

    def __init__(self, pre_command: str = None):
        super().__init__("pip", pre_command=pre_command)

    def install(self, requirements: Union[List[str], str], allow_pipes_from=None):

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
                all_pipes = read_all_pipes(allow_pipes_from)
                super().run(f"install -e {' '.join([p.setup_py_folder for p in all_pipes.values() if p.name in pipes])}")
