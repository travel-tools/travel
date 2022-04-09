import logging
import os
import shutil

from garden.cli.base import GardenCommand
from garden.config.pipe import Pipe
from garden.custom.scopes.scoped_venvs import ScopedVirtualenvs
from garden.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


class Cleaner(GardenCommand):

    def _phase_name(self):
        return "clean"

    def _perform_tasks(self, pipe: Pipe, step: str):
        if step == "post":
            pass
        else:
            super()._perform_tasks(pipe, step)

    def _manage(self, pipe: Pipe):

        logger.info(f"Cleaning {pipe.name}")
        to_remove = [
            os.path.join(pipe.setup_py_folder, f"{pipe.package}.egg-info"),     # egg-info
            Virtualenv(pipe).path,                                              # venv folder
            pipe.build_folder                                                   # artifacts build folder
        ]

        # If with scopes, remove them too
        if pipe.scopes:
            scopes = ScopedVirtualenvs(pipe)
            for env in scopes.envs.values():
                to_remove.append(env.path)

        # Clean
        for path in to_remove:
            if os.path.isdir(path):
                shutil.rmtree(path)

