import os
import shutil
from pathlib import Path
from typing import Dict, Any

import yaml
from travel.cli import planner
from travel.config.reader import BAG_FILE


def test_plan(data_location):

    # Folders and files
    plan_folder = Path(data_location)/"plan"
    travel_file_location = plan_folder/"complex"
    travel_file = travel_file_location/"travel.yml"
    name = "example"

    # Create the bags
    planner.run(travel_file_location, name)
    output_folder = travel_file_location/name

    # Check the bags structure against the plan file
    with open(travel_file) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    _is_created(output_folder, yml)

    # Cleanup
    shutil.rmtree(output_folder)


def _is_created(context: Path, yml: Dict[str, Any]):

    assert context.is_dir()
    assert (context/BAG_FILE).is_file()

    for bag, properties in yml.items():
        if "plan" not in properties:
            _is_created(context/bag, properties)


