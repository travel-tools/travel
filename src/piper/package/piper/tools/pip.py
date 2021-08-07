from piper.tools.executable import Executable


class Pip(Executable):

    def __init__(self, pre_command: str = None):
        super().__init__("pip", pre_command=pre_command)

