import logging
import os

from piper.cli.setupper import Setupper
from piper.tools.python import main_python
from piper.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


def run(context: str, package: str, command: str):

    # Setup the pipes and dependencies
    current_pipe, all_pipes = Setupper().manage(context, package=package)

    # Run the code
    env = Virtualenv(all_pipes[package])
    if os.path.isdir(env.path):
        python = env.python
    else:
        python = main_python

    # Good in unix
    if os.name == "posix":
        python.replace_process(command)
    else:
        logger.error(f" !!! Run the same command with {python.path}")
