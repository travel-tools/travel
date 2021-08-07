import logging
import os
import subprocess
import shlex

from piper.tools.shell import Shell

logger = logging.getLogger(__name__)


class Executable(Shell):

    def __init__(self, tool: str, pre_command: str = None):
        super().__init__(pre_command)
        self._tool = tool

    def run(self, command: str) -> subprocess.CompletedProcess:
        return super().run(f"{self._tool} {command}")
