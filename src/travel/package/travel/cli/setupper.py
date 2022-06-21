from travel.cli.base import TravelCommand
from travel.config.bag import Bag
from travel.custom.scopes.scoped_venvs import ScopedVirtualenvs
from travel.tools.venv import Virtualenv


class Setupper(TravelCommand):

    def _phase_name(self) -> str:
        return "setup"

    def _manage(self, bag: Bag):

        # Create the virtualenv
        venv = Virtualenv(bag, touch_requirements_file=True)
        venv.create()
        updated = venv.update()

        # Pip freeze
        if updated:
            venv.freeze()

        # Create the scopes
        if bag.scopes:
            scopes = ScopedVirtualenvs(bag, touch_requirements_file=True)
            for scope in bag.scopes:
                scopes.create(scope)
                updated = scopes.update(scope)
                if updated:
                    scopes.freeze(scope)

