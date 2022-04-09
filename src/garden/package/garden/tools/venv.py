from garden.config.pipe import Pipe
from garden.tools.base_venv import BaseVirtualenv
from garden.tools.python import Python
from garden.tools.python import main_python as default_python


class Virtualenv(BaseVirtualenv):

    def __init__(self, pipe: Pipe, main_python: Python = default_python, touch_requirements_file: bool = False):
        super().__init__(
            location=pipe.location,
            name_suffix=pipe.name,
            pip_config=pipe.pip,
            dependencies=pipe.flat_dependencies(with_current=True),
            requirements_file=pipe.requirements_file,
            main_python=main_python,
            touch_requirements_file=touch_requirements_file
        )
