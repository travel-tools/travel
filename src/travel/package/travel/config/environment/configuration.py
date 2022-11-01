import logging
import os
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


_TRAVEL_FOLDER = ".travel"
_TRAVEL_FILE = "config.yml"


class EnvironmentConfig:

    def __init__(self, yml: dict):

        # Pop the config entries
        config = yml.copy()
        self.python = config.pop("python", {})

        # If there are still configs, they are unknown. Print a warning (for retro-compatibility)
        if config:
            logger.warning(f"Unknown configuration in global travel config: {config}")


def _read(path: str = None) -> EnvironmentConfig:

    # Get global travel config from env var or default location
    path = Path(path or get_config_file_path())

    # If file exists, read it, or return an empty config
    if path.exists():
        with open(path) as f:
            yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
    else:
        yml = {}

    return EnvironmentConfig(yml)


def get_config_file_path() -> Path:
    return Path(os.environ.get(
        "TRAVEL_CONFIG_PATH",
        Path.home()/_TRAVEL_FOLDER/_TRAVEL_FILE
    ))


travel_config = _read()
