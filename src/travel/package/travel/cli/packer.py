import logging
import os
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

import setuptools
from travel.cli.setupper import Setupper
from travel.cli.utils.package import get_egg_info_folders, EGG_INFO_SUFFIX
from travel.config.bag import Bag
from travel.config.reader import parse_bags
from travel.custom.tasks import performer
from travel.tools.python import main_python

logger = logging.getLogger(__name__)

MANIFEST = "MANIFEST.in"
SETUP_PY = "setup.py"


def _find_code_and_data(dep: Bag, package: str):

    # Get all the files that should be in the dependency (code and package_data)
    egg_info = f"{package}{EGG_INFO_SUFFIX}"
    sources = os.path.join(dep.setup_py_folder, egg_info, "SOURCES.txt")  # This file is created by setup
    with open(sources, "r") as f:
        files = f.read().splitlines()

    # Get just the unique folders starting with the package name (and are not egg info)
    folders = set([
        os.path.dirname(f) for f in files
        if f.startswith(package) and not f.startswith(egg_info)
    ])

    # Find code packages
    code_packages = set([p for p in setuptools.find_packages(where=dep.setup_py_folder) if "." not in p])

    # Find package_data
    package_data = folders - code_packages

    # Return the list
    return list(code_packages), list(package_data)


def create_egg_info(current_bag: Bag):
    for bag in current_bag.flat_dependencies(with_current=True):
        setup_py = os.path.join(bag.setup_py_folder, SETUP_PY)
        main_python.run(f"{setup_py} egg_info", cwd=bag.setup_py_folder)


def _get_package_name(bag: Bag) -> str:
    # Get egg info folder (this function is always called after setup.py egg_info
    egg_infos = get_egg_info_folders(bag.setup_py_folder)
    if len(egg_infos) > 1:
        raise RuntimeError("WARNING: multiple egg_info. Run a 'travel clean' and than this command again.")
    # Get just the package name, removing the last part (EGG_INFO_SUFFIX)
    return egg_infos[0][:-len(EGG_INFO_SUFFIX)]


def pack(context: str, command: str, target: str = None, setup: bool = True):

    # Setup the bags and dependencies
    if setup:
        current_bag, all_bags = Setupper().manage(context, target=target)
    else:
        # If no setup, create just the egg_info folder for SOURCES.txt information for each dependency (and current)
        current_bag, all_bags = parse_bags(context, target)
        create_egg_info(current_bag)

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
    manifest_first_time = True
    for dep in current_bag.flat_dependencies():

        # Find code packages and package_data
        package = _get_package_name(dep)
        code, data = _find_code_and_data(dep, package)

        # Copy it inside the copied setup.py folder
        for folder in code:
            _copy_folder(
                os.path.join(dep.setup_py_folder, folder),
                os.path.join(source_build_folder)
            )

        # Store the package_data information
        manifest = [f"include {d}/*" for d in data]
        with open(manifest_file, "a") as f:
            # Write the comment for ease of documentation
            if manifest and manifest_first_time:
                f.write(f"\n#travel-dependency")
                manifest_first_time = False
            # Add each package_data
            f.write("\n"+"\n".join(manifest))  # Add a \n in case file is not ending with that

    # Instead of pack
    skip = performer.perform_tasks("pack", "instead", current_bag)

    # If no instead steps
    if not skip:
        # Setup the code
        setup_py = os.path.join(source_build_folder, SETUP_PY)
        main_python.run(f"{setup_py} {' '.join(command)}", cwd=source_build_folder)  # TODO should check for spaces and commas, or use list!

    # Post-pack
    performer.perform_tasks("pack", "post", current_bag)


def _copy_folder(source, destination):
    os.makedirs(destination, exist_ok=True)
    right_destination = os.path.join(destination, os.path.basename(os.path.normpath(source)))
    return copy_tree(source, right_destination)
