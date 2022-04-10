from travel.config.bag import Bag
from travel.tools.base_venv import BaseVirtualenv
from travel.tools.python import Python
from travel.tools.python import main_python as default_python


class Virtualenv(BaseVirtualenv):

    def __init__(self, bag: Bag, main_python: Python = default_python, touch_requirements_file: bool = False):
        super().__init__(
            location=bag.location,
            name_suffix=bag.name,
            pip_config=bag.pip,
            dependencies=bag.flat_dependencies(with_current=True),
            requirements_file=bag.requirements_file,
            main_python=main_python,
            touch_requirements_file=touch_requirements_file
        )
