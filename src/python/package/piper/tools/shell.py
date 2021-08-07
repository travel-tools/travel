import logging
import os
import subprocess
import shlex


logger = logging.getLogger(__name__)


class Shell:

    def __init__(self, pre_command: str = None):
        self._pre_command = f"{pre_command} && " if pre_command else ""

    def run(self, command: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            self._pre_command + command,
            check=True,
            capture_output=True,
            text=True,
            shell=True
        )
