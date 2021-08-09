import logging
import subprocess

from piper.tools.shell import Shell

logger = logging.getLogger(__name__)


class Executable(Shell):

    def __init__(self, tool: str, pre_command: str = None):
        super().__init__(pre_command)
        self._tool = tool

    def run(self, command: str, capture: bool = False, text: bool = True, cwd: str = None) -> subprocess.CompletedProcess:
        return super().run(f"{self._tool} {command}", capture=capture, text=text, cwd=cwd)
