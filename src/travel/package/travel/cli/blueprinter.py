import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List

import pkg_resources
import yaml
from travel import RESOURCES_LOCATION
from travel.config.bag import Nest
from travel.config.reader import BAG_FILE
from travel.config.sanitizers import pip_sanitizer, name_sanitizer
from travel.tools.venv import Virtualenv

logger = logging.getLogger(__name__)
_GENERATE_BLUEPRINT = os.path.join(RESOURCES_LOCATION, "blueprint", "generate.py")


def _generate_breath_first(blueprint_file: str, venv: Virtualenv, context: str, yml: Dict[str, Any], local_blueprints: List[str] = None):

    # Generate these blueprints
    for bag, properties in yml.items():

        # Get the folder where the bag will be created
        bag = name_sanitizer.sanitize_name(bag)
        bag_context = os.path.join(context, bag)

        # Is it a blueprint?
        if "blueprint" in properties:

            # Get the package of the blueprint
            blueprint = properties["blueprint"]
            name = pip_sanitizer.sanitize_versioned_package(blueprint)
            venv.pip.install(name, allow_bags_from=local_blueprints)

            # Generate the blueprint
            command = f'"{_GENERATE_BLUEPRINT}" --context "{bag_context}" --blueprint {name} --file "{blueprint_file}" --bag {bag}'
            venv.python.run(command)

    # Create the "folder" bag.yml file
    bag_file = os.path.join(context, BAG_FILE)
    if not os.path.isfile(bag_file):
        Path(bag_file).touch()

    # Generate the subbags
    for bag, properties in yml.items():
        bag_context = os.path.join(context, bag)
        if "bags" in properties:
            _generate_breath_first(blueprint_file, venv, bag_context, properties["bags"], local_blueprints=local_blueprints)


def run(context: str, local_blueprints: List[str] = None):

    # Temporary create a venv
    venv = Virtualenv(Nest(location=context, yml={}))
    venv.create()
    version = pip_sanitizer.sanitize_version(pkg_resources.get_distribution("PyYAML").version)
    venv.pip.install(f"PyYAML=={version}")

    # Read the blueprint file
    path = os.path.join(context, "blueprint.yml")
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    if not yml or "bags" not in yml:
        raise ValueError("Blueprint file must not be empty and should contain at least 'bags' key.")

    # Generate
    _generate_breath_first(path, venv, context, yml["bags"], local_blueprints=local_blueprints)

    # Remove the temporary venv
    shutil.rmtree(venv.path)
