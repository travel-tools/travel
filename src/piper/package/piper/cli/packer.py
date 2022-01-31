import logging
import os
import shutil
from distutils.dir_util import copy_tree

import setuptools
from piper.cli.setupper import Setupper
from piper.custom.tasks import performer
from piper.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


def pack(context: str, command: str, package: str = None):

    # Setup the pipes and dependencies
    current_pipe, all_pipes = Setupper().manage(context, package=package)

    # Pre-pack
    performer.perform_tasks("pack", "pre", current_pipe)

    # Get the right python (this might be useful in case the setup.py uses a particular syntax)
    env = Virtualenv(current_pipe)

    # Clean the previous target folder, if existing
    build_folder = current_pipe.build_folder
    if os.path.isdir(build_folder):
        shutil.rmtree(build_folder)

    # Copy the structure of this package
    _copy_folder(current_pipe.setup_py_folder, build_folder)
    source_build_folder = os.path.join(build_folder, os.path.basename(current_pipe.setup_py_folder))
    # For all dependencies, copy their code too
    for dep in current_pipe.flat_dependencies():
        # For all code packages, copy it inside the copied setup.py folder
        for folder in [p for p in setuptools.find_packages(where=dep.setup_py_folder) if "." not in p]:
            _copy_folder(
                os.path.join(dep.setup_py_folder, folder),
                os.path.join(source_build_folder)
            )

    # Setup the code
    setup_py = os.path.join(source_build_folder, "setup.py")
    env.python.run(f"{setup_py} {' '.join(command)}", cwd=source_build_folder)  # TODO should check for spaces and commas, or use list!

    # Post-pack
    performer.perform_tasks("pack", "post", current_pipe)


def _copy_folder(source, destination):
    os.makedirs(destination, exist_ok=True)
    right_destination = os.path.join(destination, os.path.basename(os.path.normpath(source)))
    return copy_tree(source, right_destination)
