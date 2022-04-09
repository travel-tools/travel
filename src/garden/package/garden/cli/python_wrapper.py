import logging
import os

from garden.cli.setupper import Setupper
from garden.tools.python import main_python
from garden.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


def run(context: str, package: str, command: str):

    # Setup the nests and dependencies
    current_nest, all_nests = Setupper().manage(context, package=package)

    # Run the code
    env = Virtualenv(all_nests[package])
    if os.path.isdir(env.path):
        python = env.python
    else:
        python = main_python

    # Good in unix
    if os.name == "posix":
        python.replace_process(command)
    else:
        logger.error(f" !!! Run the same command with {python.path}")
