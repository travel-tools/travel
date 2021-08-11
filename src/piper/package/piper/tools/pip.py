import os
from typing import Dict

from piper.tools.executable import Executable
from piper.config.sanitizers.pip_sanitizer import sanitize_package, sanitize_version

class Pip(Executable):

    def __init__(self, pre_command: str = None):
        super().__init__("pip", pre_command=pre_command)

    def install(self, requirements: Dict[str, str], allow_local_files=False):
        packages = [
            version if allow_local_files and os.path.isdir(version) else f'{sanitize_package(name)}=={sanitize_version(version)}'
            for name, version in requirements.items()
        ]
        super().run(f"install {' '.join(packages)}")
