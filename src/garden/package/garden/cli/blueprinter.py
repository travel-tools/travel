import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List

import pkg_resources
import yaml
from garden import RESOURCES_LOCATION
from garden.config.nest import Nest
from garden.config.reader import NEST_FILE
from garden.config.sanitizers import pip_sanitizer, name_sanitizer
from garden.tools.venv import Virtualenv

logger = logging.getLogger(__name__)
_GENERATE_BLUEPRINT = os.path.join(RESOURCES_LOCATION, "blueprint", "generate.py")


def _generate_breath_first(blueprint_file: str, venv: Virtualenv, context: str, yml: Dict[str, Any], local_blueprints: List[str] = None):

    # Generate these blueprints
    for nest, properties in yml.items():

        # Get the folder where the nest will be created
        nest = name_sanitizer.sanitize_name(nest)
        nest_context = os.path.join(context, nest)

        # Is it a blueprint?
        if "blueprint" in properties:

            # Get the package of the blueprint
            blueprint = properties["blueprint"]
            name = pip_sanitizer.sanitize_versioned_package(blueprint)
            venv.pip.install(name, allow_nests_from=local_blueprints)

            # Generate the blueprint
            command = f'"{_GENERATE_BLUEPRINT}" --context "{nest_context}" --blueprint {name} --file "{blueprint_file}" --nest {nest}'
            venv.python.run(command)

    # Create the "folder" nest.yml file
    nest_file = os.path.join(context, NEST_FILE)
    if not os.path.isfile(nest_file):
        Path(nest_file).touch()

    # Generate the subnests
    for nest, properties in yml.items():
        nest_context = os.path.join(context, nest)
        if "nests" in properties:
            _generate_breath_first(blueprint_file, venv, nest_context, properties["nests"], local_blueprints=local_blueprints)


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
    if not yml or "nests" not in yml:
        raise ValueError("Blueprint file must not be empty and should contain at least 'nests' key.")

    # Generate
    _generate_breath_first(path, venv, context, yml["nests"], local_blueprints=local_blueprints)

    # Remove the temporary venv
    shutil.rmtree(venv.path)
