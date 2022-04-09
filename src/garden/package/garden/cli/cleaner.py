import logging
import os
import shutil

from garden.cli.base import GardenCommand
from garden.config.nest import Nest
from garden.custom.scopes.scoped_venvs import ScopedVirtualenvs
from garden.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


class Cleaner(GardenCommand):

    def _phase_name(self):
        return "clean"

    def _perform_tasks(self, nest: Nest, step: str):
        if step == "post":
            pass
        else:
            super()._perform_tasks(nest, step)

    def _manage(self, nest: Nest):

        logger.info(f"Cleaning {nest.name}")
        to_remove = [
            os.path.join(nest.setup_py_folder, f"{nest.package}.egg-info"),     # egg-info
            Virtualenv(nest).path,                                              # venv folder
            nest.build_folder                                                   # artifacts build folder
        ]

        # If with scopes, remove them too
        if nest.scopes:
            scopes = ScopedVirtualenvs(nest)
            for env in scopes.envs.values():
                to_remove.append(env.path)

        # Clean
        for path in to_remove:
            if os.path.isdir(path):
                shutil.rmtree(path)

