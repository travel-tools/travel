import logging
import os

from travel.cli.setupper import Setupper
from travel.tools.python import main_python
from travel.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


def run(context: str, package: str, command: str):

    # Setup the bags and dependencies
    current_bag, all_bags = Setupper().manage(context, package=package)

    # Run the code
    env = Virtualenv(all_bags[package])
    if os.path.isdir(env.path):
        python = env.python
    else:
        python = main_python

    # Good in unix
    if os.name == "posix":
        python.replace_process(command)
    else:
        logger.error(f" !!! Run the same command with {python.path}")
