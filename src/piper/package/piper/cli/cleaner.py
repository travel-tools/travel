import logging
import os
import shutil

from piper.cli.base import PiperCommand
from piper.config.pipe import Pipe
from piper.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


class Cleaner(PiperCommand):

    def _manage(self, pipe: Pipe):

        logger.info(f"Cleaning {pipe.name}")
        to_remove = [
            os.path.join(pipe.setup_py_folder, f"{pipe.package}.egg-info"),     # egg-info
            Virtualenv(pipe).path,                                              # venv folder
            pipe.build_folder                                                   # artifacts build folder
        ]

        # Clean
        for path in to_remove:
            if os.path.isdir(path):
                shutil.rmtree(path)
