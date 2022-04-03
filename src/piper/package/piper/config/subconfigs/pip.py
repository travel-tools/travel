import logging

from piper.config.sanitizers import pip_sanitizer

logger = logging.getLogger(__name__)


class PipConfig:

    def __init__(self, config: dict):
        self.version = pip_sanitizer.sanitize_pip_version(config.pop("version", None), nullable=True)

        # If there are still configs, they are unknown. Print a warning
        if config:
            logger.warning(f"Unknown configuration for pip: {config}")
