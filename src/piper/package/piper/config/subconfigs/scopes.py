import logging

from piper.config.sanitizers import pip_sanitizer


logger = logging.getLogger(__name__)


class ScopeConfig:

    def __init__(self, name: str, config: dict):
        self.name = name
        self.requirements = [pip_sanitizer.sanitize_versioned_package(req) for req in config.pop("requirements", {})]

        # If there are still configs, they are unknown. Print a warning
        if config:
            logger.warning(f"Unknown configuration for scope \"{name}\": {config}")
