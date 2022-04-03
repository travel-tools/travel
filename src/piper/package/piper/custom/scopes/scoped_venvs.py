import os

from piper.config.pipe import Pipe
from piper.tools.base_venv import BaseVirtualenv
from piper.tools.python import Python
from piper.tools.python import main_python as default_python


class ScopedVirtualenvs():

    def __init__(self, pipe: Pipe, main_python: Python = default_python, touch_requirements_file: bool = False):
        self.envs = {
            scope: BaseVirtualenv(
                location=pipe.location,
                name_suffix=f"{pipe.name}-{scope}",
                pip_config=pipe.pip,
                dependencies=pipe.flat_dependencies(with_current=True),
                requirements_file=os.path.join(pipe.location, f"requirements_{scope}.txt"),
                main_python=main_python,
                touch_requirements_file=touch_requirements_file,
                extra_requirements=config.requirements
            )
            for scope, config in pipe.scopes.items()
        }

    def create(self, scope: str):
        self.envs[scope].create()

    def create_all(self):
        for scope in self.envs.keys():
            self.create(scope)

    def update(self, scope: str):
        self.envs[scope].update()

    def update_all(self):
        for scope in self.envs.keys():
            self.update(scope)

    def freeze(self, scope: str):
        self.envs[scope].freeze()

    def freeze_all(self):
        for scope in self.envs.keys():
            self.freeze(scope)
