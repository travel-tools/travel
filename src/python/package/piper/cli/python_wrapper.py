import logging
import os

from piper.cli.setupper import Setupper
from piper.tools.python import main_python
from piper.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


def run(pipe_location: str, package: str, command: str = None):

    # Setup the pipes and dependencies
    current_pipe, all_pipes = Setupper().manage(pipe_location)

    # Run the code
    env = Virtualenv(all_pipes[package])
    if os.path.isdir(env.path):
        python = env.python
    else:
        python = main_python
    python.run(command)
