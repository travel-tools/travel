import os
from pathlib import Path

from garden.cli.base import GardenCommand
from garden.config.nest import Nest
from garden.custom.scopes.scoped_venvs import ScopedVirtualenvs
from garden.tools.venv import Virtualenv


class Setupper(GardenCommand):

    def _phase_name(self) -> str:
        return "setup"

    def _manage(self, nest: Nest):

        # Create the virtualenv
        venv = Virtualenv(nest, touch_requirements_file=True)
        venv.create()
        updated = venv.update()

        # Pip freeze
        if updated:
            venv.freeze()

        # Create the scopes
        if nest.scopes:
            scopes = ScopedVirtualenvs(nest, touch_requirements_file=True)
            for scope in nest.scopes:
                scopes.create(scope)
                updated = scopes.update(scope)
                if updated:
                    scopes.freeze(scope)

