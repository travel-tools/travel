from garden.config.nest import Nest
from garden.tools.base_venv import BaseVirtualenv
from garden.tools.python import Python
from garden.tools.python import main_python as default_python


class Virtualenv(BaseVirtualenv):

    def __init__(self, nest: Nest, main_python: Python = default_python, touch_requirements_file: bool = False):
        super().__init__(
            location=nest.location,
            name_suffix=nest.name,
            pip_config=nest.pip,
            dependencies=nest.flat_dependencies(with_current=True),
            requirements_file=nest.requirements_file,
            main_python=main_python,
            touch_requirements_file=touch_requirements_file
        )
