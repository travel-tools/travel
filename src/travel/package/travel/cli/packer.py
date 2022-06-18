import logging
import os
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

import setuptools
from travel.cli.setupper import Setupper
from travel.config.bag import Bag
from travel.config.reader import parse_bags
from travel.custom.tasks import performer
from travel.tools.python import main_python
from travel.tools.venv import Virtualenv

logger = logging.getLogger(__name__)

MANIFEST = "MANIFEST.in"


def _find_code_and_data(dep: Bag):

    # Get all the files that should be in the dependency (code and package_data)
    egg_info = f"{dep.package}.egg-info"
    sources = os.path.join(dep.setup_py_folder, egg_info, "SOURCES.txt")  # This file is created by setup
    with open(sources, "r") as f:
        files = f.read().splitlines()

    # Get just the unique folders starting with the package name (and are not egg info)
    folders = set([
        os.path.dirname(f) for f in files
        if f.startswith(dep.package) and not f.startswith(egg_info)
    ])

    # Find code packages
    code_packages = set([p for p in setuptools.find_packages(where=dep.setup_py_folder) if "." not in p])

    # Find package_data
    package_data = folders - code_packages

    # Return the list
    return list(code_packages), list(package_data)


def pack(context: str, command: str, target: str = None, setup: bool = True):

    # Setup the bags and dependencies
    if setup:
        current_bag, all_bags = Setupper().manage(context, target=target)
    else:
        current_bag, all_bags = parse_bags(context, target)
        Virtualenv(current_bag).create()

    # Pre-pack
    performer.perform_tasks("pack", "pre", current_bag)

    # Clean the previous target folder, if existing
    build_folder = current_bag.build_folder
    if os.path.isdir(build_folder):
        shutil.rmtree(build_folder)

    # Copy the structure of this package
    _copy_folder(current_bag.setup_py_folder, build_folder)

    # Copy the MANIFEST.in
    source_build_folder = os.path.join(build_folder, os.path.basename(current_bag.setup_py_folder))
    manifest_file = os.path.join(source_build_folder, MANIFEST)
    Path(manifest_file).touch(exist_ok=True)

    # For all dependencies, copy their code and package_data too
    for dep in current_bag.flat_dependencies():

        # Find code packages and package_data
        code, data = _find_code_and_data(dep)

        # Copy it inside the copied setup.py folder
        for folder in code:
            _copy_folder(
                os.path.join(dep.setup_py_folder, folder),
                os.path.join(source_build_folder)
            )

        # Store the package_data information
        manifest = [f"include {d}/*" for d in data]
        with open(manifest_file, "a") as f:
            f.writelines(manifest)

    # Setup the code
    setup_py = os.path.join(source_build_folder, "setup.py")
    main_python.run(f"{setup_py} {' '.join(command)}", cwd=source_build_folder)  # TODO should check for spaces and commas, or use list!

    # Post-pack
    performer.perform_tasks("pack", "post", current_bag)


def _copy_folder(source, destination):
    os.makedirs(destination, exist_ok=True)
    right_destination = os.path.join(destination, os.path.basename(os.path.normpath(source)))
    return copy_tree(source, right_destination)
