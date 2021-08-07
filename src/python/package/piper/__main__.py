import argparse
import logging
import os
from enum import Enum

from piper.cli import python_wrapper
from piper.cli.cleaner import Cleaner
from piper.cli.setupper import Setupper

logger = logging.getLogger(__name__)


def main():

    # Piper
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", default=os.getcwd(), help="Path to the folder containing the pipe.yml file")
    parser.set_defaults(action=lambda args: parser.parse_args(["-h"]))
    subparsers = parser.add_subparsers()

    # Clean
    clean = subparsers.add_parser("clean")
    clean.set_defaults(action=lambda args, rest: Cleaner().manage(args.context))

    # Setup
    setup = subparsers.add_parser("setup")
    setup.set_defaults(action=lambda args, rest: Setupper().manage(args.context))

    # Python
    python = subparsers.add_parser("python")
    python.add_argument("package", help="Name of the pipe (it will be used to activate its venv)")
    # Since OS parses the quotes before getting here, we know that if a command in argv had spaces, the user called it with quotes. Put it there again.
    python.set_defaults(action=lambda args, rest: python_wrapper.run(args.context, args.package, ' '.join([f'"{arg}"' if ' ' in arg else arg for arg in rest])))

    # Parse args and invoke the corresponding functions
    arguments, remainder = parser.parse_known_args()
    arguments.action(arguments, remainder)
    logger.info("All done.")


if __name__ == '__main__':
    main()
