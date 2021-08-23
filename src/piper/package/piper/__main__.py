import argparse
import logging
import os

from piper.cli import python_wrapper, blueprinter, packer
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

    # Blueprint
    blueprint = subparsers.add_parser("blueprint")
    blueprint.set_defaults(action=lambda args, rest: blueprinter.run(args.context))

    # Setup
    setup = subparsers.add_parser("setup")
    setup.set_defaults(action=lambda args, rest: Setupper().manage(args.context))

    # Pack
    pack = subparsers.add_parser("pack")
    pack.add_argument("package", help="Name of the pipe to run setup.py commands")
    pack.set_defaults(action=lambda args, rest: packer.pack(args.context, args.package, rest))

    # Release

    # # Python
    # python = subparsers.add_parser("python")
    # python.add_argument("package", help="Name of the pipe (it will be used to activate its venv)")
    # python.set_defaults(action=lambda args, rest: python_wrapper.run(args.context, args.package, rest))

    # Parse args and invoke the corresponding functions
    arguments, remainder = parser.parse_known_args()
    arguments.action(arguments, remainder)
    logger.info("All done.")


if __name__ == '__main__':
    main()
