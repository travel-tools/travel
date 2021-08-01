import os
import sys


class Python:

    def __init__(self, path: str = None):
        self.path = path or os.environ.get("PIPER_PYTHON_PATH", sys.executable)
        # TODO version from Popen


main_python = Python()
