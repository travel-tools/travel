import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Any

import pkg_resources
import yaml
from piper import RESOURCES_LOCATION
from piper.config.pipe import Pipe
from piper.config.sanitizers import pip_sanitizer, pipe_sanitizer
from piper.tools.venv import Virtualenv

logger = logging.getLogger(__name__)
_GENERATE_BLUEPRINT = os.path.join(RESOURCES_LOCATION, "blueprint", "generate.py")


def _generate_breath_first(blueprint_file: str, venv: Virtualenv, context: str, yml: Dict[str, Any]):

    # Generate these blueprints
    for pipe, properties in yml.items():

        # Create the directory
        pipe = pipe_sanitizer.sanitize_name(pipe)
        pipe_context = os.path.join(context, pipe)
        os.makedirs(pipe_context, exist_ok=True)

        # Is it a blueprint?
        if "blueprint" in properties:

            # Get the package of the blueprint
            name, version = str(properties["blueprint"]).split("==", maxsplit=1)
            name = pip_sanitizer.sanitize_package(name)
            version = pip_sanitizer.sanitize_version(version)
            venv.pip.run(f"install {name}=={version}")

            # Generate the blueprint
            command = f'"{_GENERATE_BLUEPRINT}" --context "{pipe_context}" --blueprint {name} --file "{blueprint_file}" --pipe {pipe}'
            print(command)
            venv.python.run(f'"{_GENERATE_BLUEPRINT}" --context "{pipe_context}" --blueprint {name} --file "{blueprint_file}" --pipe {pipe}')

    # Generate the subpipes
    for pipe, properties in yml.items():
        pipe_context = os.path.join(context, pipe)
        if "pipes" in properties:
            _generate_breath_first(blueprint_file, venv, pipe_context, properties["pipes"])


def run(context: str):

    # Temporary create a venv
    venv = Virtualenv(Pipe(location=context, yml={}))
    venv.create()
    version = pip_sanitizer.sanitize_version(pkg_resources.get_distribution("PyYAML").version)
    venv.pip.run(f"install PyYAML=={version}")

    # Read the blueprint file
    path = os.path.join(context, "blueprint.yml")
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    if not yml or "pipes" not in yml:
        raise ValueError("Blueprint file must not be empty and should contain at least 'pipes' key.")

    # Generate
    _generate_breath_first(path, venv, context, yml["pipes"])

    # Remove the temporary venv
    shutil.rmtree(venv.path)
