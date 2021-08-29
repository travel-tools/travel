from pathlib import Path
from typing import Dict, Any

from pipertask.task import PiperTask


class PiperTaskExample(PiperTask):

    def perform(self, context: Path, config: Dict[str, Any]) -> None:
        print(f"I would perform my actions in {context} with this configs: {config}")
