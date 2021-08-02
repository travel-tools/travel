import subprocess


class VirtualenvTool:

    def __init__(self, tool: str, pre_command: str = None):
        self._tool = tool
        self._pre_command = pre_command

    def run(self, command: str) -> str:
        return subprocess.run(
            (f"{self._pre_command} && " if self._pre_command else "") + f"{self._tool} {command}",
            check=True,
            shell=True,
            capture_output=True
        ).stdout.decode("utf-8")
