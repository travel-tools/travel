import os
from pathlib import Path

from piper.cli.base import PiperCommand
from piper.config.pipe import Pipe
from piper.tools.venv import Virtualenv


class Setupper(PiperCommand):

    def _manage(self, pipe: Pipe):

        # Prepare the requirements file
        if not os.path.isfile(pipe.requirements_file):
            Path(pipe.requirements_file).touch()

        # Create the virtualenv
        venv = Virtualenv(pipe)
        venv.create()
        venv.update()

        # Pip freeze
        venv.freeze()
