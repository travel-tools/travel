from pathlib import Path
from typing import Dict, Any

from gardentask.task import GardenTask


class GardenTaskExample(GardenTask):

    def perform(self, context: Path, config: Dict[str, Any]) -> None:
        print(f"I would perform my actions in {context} with this configs: {config}")
