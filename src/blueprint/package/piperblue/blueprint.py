import abc
from typing import Dict, Any


class PiperBlueprint(abc.ABC):

    @abc.abstractmethod
    def generate(self, context: str, blueprint: Dict[str, Any]) -> None:
        pass

