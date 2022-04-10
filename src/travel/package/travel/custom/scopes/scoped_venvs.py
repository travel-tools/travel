import os

from travel.config.bag import Bag
from travel.tools.base_venv import BaseVirtualenv
from travel.tools.python import Python
from travel.tools.python import main_python as default_python


class ScopedVirtualenvs():

    def __init__(self, bag: Bag, main_python: Python = default_python, touch_requirements_file: bool = False):
        self.envs = {
            scope: BaseVirtualenv(
                location=bag.location,
                name_suffix=f"{bag.name}-{scope}",
                pip_config=bag.pip,
                dependencies=bag.flat_dependencies(with_current=True),
                requirements_file=os.path.join(bag.location, f"requirements_{scope}.txt"),
                main_python=main_python,
                touch_requirements_file=touch_requirements_file,
                extra_requirements=config.requirements
            )
            for scope, config in bag.scopes.items()
        }

    def create(self, scope: str):
        self.envs[scope].create()

    def create_all(self):
        for scope in self.envs.keys():
            self.create(scope)

    def update(self, scope: str) -> bool:
        return self.envs[scope].update()

    def update_all(self):
        for scope in self.envs.keys():
            self.update(scope)

    def freeze(self, scope: str):
        self.envs[scope].freeze()

    def freeze_all(self):
        for scope in self.envs.keys():
            self.freeze(scope)
