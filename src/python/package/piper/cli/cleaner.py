import logging
import os
import shutil

from piper.cli.base import PiperCommand
from piper.config.pipe import Pipe
from piper.tools.python import main_python
from piper.tools.venv import Virtualenv


logger = logging.getLogger(__name__)


class Cleaner(PiperCommand):

    def _manage(self, pipe: Pipe):

        logger.info(f"Cleaning {pipe.name}")
        to_remove = [
            os.path.join(pipe.setup_py_folder, f"{pipe.package}.egg-info"),     # egg-info
            Virtualenv(main_python=main_python, pipe=pipe).path                 # venv folder
        ]

        # Clean
        for path in to_remove:
            if os.path.isdir(path):
                shutil.rmtree(path)
