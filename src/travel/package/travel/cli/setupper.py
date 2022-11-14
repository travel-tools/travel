import logging

from travel.cli.base import TravelCommand
from travel.config.bag import Bag
from travel.config.environment.python import get_right_python
from travel.config.project import Project
from travel.custom.scopes.scoped_venvs import ScopedVirtualenvs
from travel.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


class Setupper(TravelCommand):

    def _phase_name(self) -> str:
        return "setup"

    def _manage(self, bag: Bag, project: Project):

        # Get the python to use
        python = get_right_python(project)

        # Create the virtualenv
        venv = Virtualenv(bag, main_python=python, touch_requirements_file=True)
        venv.create()
        updated = venv.update()

        # Pip freeze
        if updated:
            venv.freeze()

        # Create the scopes
        if bag.scopes:
            scopes = ScopedVirtualenvs(bag, main_python=python, touch_requirements_file=True)
            for scope in bag.scopes:
                scopes.create(scope)
                updated = scopes.update(scope)
                if updated:
                    scopes.freeze(scope)

