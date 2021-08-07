import argparse
import logging
import os
from enum import Enum

from piper.cli import runner
from piper.cli.cleaner import Cleaner
from piper.cli.setupper import Setupper

logger = logging.getLogger(__name__)


class Action(str, Enum):

    RUN = "run"
    SETUP = "setup"
    CLEAN = "clean"


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=[v.value for v in Action])
    parser.add_argument("--pipe", required=False)
    args, _ = parser.parse_known_args()
    return args


def main():

    # Get args
    args = get_args()

    # Parse
    action = args.action
    pipe_location = args.pipe or os.getcwd()

    if action == Action.RUN:

        runner.run(pipe_location=pipe_location)

    elif action == Action.SETUP:

        Setupper().manage(pipe_location=pipe_location)

    elif action == Action.CLEAN:

        Cleaner().manage(pipe_location=pipe_location)

    else:

        raise RuntimeError(f"Action {action} unknown")

    logger.info("All done.")


if __name__ == '__main__':
    main()
