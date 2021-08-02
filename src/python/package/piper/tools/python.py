import os
import sys

from piper.tools.venv_tool import VirtualenvTool


class Python(VirtualenvTool):

    def __init__(self, path: str = None, pre_command: str = None):
        self.path = path or os.environ.get("PIPER_PYTHON_PATH", sys.executable)
        super().__init__(self.path, pre_command=pre_command)
        # TODO version from Popen


main_python = Python()
