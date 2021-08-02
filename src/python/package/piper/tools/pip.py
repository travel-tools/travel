from piper.tools.venv_tool import VirtualenvTool


class Pip(VirtualenvTool):

    def __init__(self, pre_command: str = None):
        super().__init__("pip", pre_command=pre_command)

