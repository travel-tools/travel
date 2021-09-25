import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List

import pkg_resources
import yaml
from piper import RESOURCES_LOCATION
from piper.config.pipe import Pipe
from piper.config.reader import PIPE_FILE
from piper.config.sanitizers import pip_sanitizer, name_sanitizer
from piper.tools.venv import Virtualenv

logger = logging.getLogger(__name__)
_GENERATE_BLUEPRINT = os.path.join(RESOURCES_LOCATION, "blueprint", "generate.py")


def _generate_breath_first(blueprint_file: str, venv: Virtualenv, context: str, yml: Dict[str, Any], local_blueprints: List[str] = None):

    # Generate these blueprints
    for pipe, properties in yml.items():

        # Get the folder where the pipe will be created
        pipe = name_sanitizer.sanitize_name(pipe)
        pipe_context = os.path.join(context, pipe)

        # Is it a blueprint?
        if "blueprint" in properties:

            # Get the package of the blueprint
            blueprint = properties["blueprint"]
            name = pip_sanitizer.sanitize_versioned_package(blueprint)
            venv.pip.install(name, allow_pipes_from=local_blueprints)

            # Generate the blueprint
            command = f'"{_GENERATE_BLUEPRINT}" --context "{pipe_context}" --blueprint {name} --file "{blueprint_file}" --pipe {pipe}'
            venv.python.run(command)

    # Create the "folder" pipe.yml file
    pipe_file = os.path.join(context, PIPE_FILE)
    if not os.path.isfile(pipe_file):
        Path(pipe_file).touch()

    # Generate the subpipes
    for pipe, properties in yml.items():
        pipe_context = os.path.join(context, pipe)
        if "pipes" in properties:
            _generate_breath_first(blueprint_file, venv, pipe_context, properties["pipes"], local_blueprints=local_blueprints)


def run(context: str, local_blueprints: List[str] = None):

    # Temporary create a venv
    venv = Virtualenv(Pipe(location=context, yml={}))
    venv.create()
    version = pip_sanitizer.sanitize_version(pkg_resources.get_distribution("PyYAML").version)
    venv.pip.install(f"PyYAML=={version}")

    # Read the blueprint file
    path = os.path.join(context, "blueprint.yml")
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    if not yml or "pipes" not in yml:
        raise ValueError("Blueprint file must not be empty and should contain at least 'pipes' key.")

    # Generate
    _generate_breath_first(path, venv, context, yml["pipes"], local_blueprints=local_blueprints)

    # Remove the temporary venv
    shutil.rmtree(venv.path)
