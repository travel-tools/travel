import logging
from typing import List

from cookiecutter.main import cookiecutter

logger = logging.getLogger(__name__)


def _validate(config):
    if "=" not in config:
        raise ValueError(f"Configs should have '=', so this is not valid: {config}")
    return config


def run(context: str, plan: str, checkout: str = None, directory: str = None, no_input: bool = False, config: List[str] = None):

    extra_context = {
        key: value
        for key, value in [
            _validate(c).split("=", maxsplit=1)
            for c in (config if config else [])
        ]
    }

    cookiecutter(
        template=plan,
        output_dir=context,
        checkout=checkout,
        directory=directory,
        no_input=no_input,
        extra_context=extra_context
    )
