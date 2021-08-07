import abc
import os
from typing import Dict, Any

import yaml


class PiperBlueprint(abc.ABC):

    def generate_from(self, context: str):

        # Read the blueprint file
        path = os.path.join(context, "blueprint.yml")
        with open(path) as f:
            yml = yaml.load(f, Loader=yaml.SafeLoader)
        if not yml:
            raise ValueError("Blueprint file must not be empty")

        # Generate
        self.generate(context, yml)

    @abc.abstractmethod
    def generate(self, context: str, blueprint: Dict[str, Any]) -> None:
        pass
