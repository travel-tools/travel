import logging
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any

import yaml
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from travel.config.reader import BAG_FILE
from travel.config.sanitizers import name_sanitizer

logger = logging.getLogger(__name__)
_PLAN = "plan"
_TRAVEL_FILE = "travel.yml"
_CONFIG = "config"


def _generate_breath_first(folder: str, yml: Dict[str, Any], local_plans: List[str] = None):

    # Generate these plans
    for bag, properties in yml.items():

        # Get the folder where the bag will be created
        bag = name_sanitizer.sanitize_name(bag)
        bag_folder = os.path.join(folder, bag)

        # Is it a plan?
        if _PLAN in properties:

            # Get the package of the plan
            plan = properties[_PLAN]
            config = properties[_CONFIG]
            cookiecutter(plan, output_dir=bag_folder, no_input=True, extra_context=config)

    # Create the "folder" bag.yml file
    bag_file = os.path.join(folder, BAG_FILE)
    if not os.path.isfile(bag_file):
        Path(bag_file).touch()

    # Generate the subbags
    for bag, properties in yml.items():
        bag_folder = os.path.join(folder, bag)
        if not (_PLAN in properties and isinstance(properties[_PLAN], str)):
            _generate_breath_first(bag_folder, properties, local_plans=local_plans)


def run(context: str, name: str, local_plans: List[str] = None):

    # Read the travel file
    travel_file = os.path.join(context, _TRAVEL_FILE)
    with open(travel_file) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    if not yml:
        raise ValueError("Travel file must not be empty.")

    # Generate
    folder = os.path.join(context, name)
    try:
        _generate_breath_first(folder, yml, local_plans=local_plans)
    except OutputDirExistsException as e:
        # If the error is just because the folder exists, exit
        raise e
    except Exception as e:
        # Remove in case of any other error
        shutil.rmtree(folder)
        raise e
