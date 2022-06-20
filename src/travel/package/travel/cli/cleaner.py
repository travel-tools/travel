import logging
import os
import shutil

from travel.cli.base import TravelCommand
from travel.cli.utils.package import get_egg_info_folders
from travel.config.bag import Bag
from travel.custom.scopes.scoped_venvs import ScopedVirtualenvs
from travel.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


class Cleaner(TravelCommand):

    def _phase_name(self):
        return "clean"

    def _perform_tasks(self, bag: Bag, step: str):
        if step == "post":
            pass
        else:
            super()._perform_tasks(bag, step)

    def _manage(self, bag: Bag):

        logger.info(f"Cleaning {bag.name}")
        to_remove = [
            Virtualenv(bag).path,                                              # venv folder
            bag.build_folder                                                   # artifacts build folder
        ]
        to_remove = to_remove + [                                              # egg_info(s)
            os.path.join(bag.setup_py_folder, f)
            for f in get_egg_info_folders(bag.setup_py_folder)
        ]

        print(to_remove)

        # If with scopes, remove them too
        if bag.scopes:
            scopes = ScopedVirtualenvs(bag)
            for env in scopes.envs.values():
                to_remove.append(env.path)

        # Clean
        for path in to_remove:
            if os.path.isdir(path):
                shutil.rmtree(path)

