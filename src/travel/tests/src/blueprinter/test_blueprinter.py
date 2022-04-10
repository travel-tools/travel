import os
import shutil
from pathlib import Path
from typing import Dict, Any

import yaml
from travel.cli import blueprinter
from travel.config.reader import BAG_FILE


def test_blueprint(data_location):

    # Folders and files
    blueprint_folder = Path(data_location)/"blueprint"
    blueprint_file_location = blueprint_folder/"complex"
    local_blueprints = blueprint_folder/"locals"
    blueprint_file = blueprint_file_location/"blueprint.yml"

    # Create the bags
    blueprinter.run(blueprint_file_location, local_blueprints=local_blueprints)

    # Check the bags structure against the blueprint file
    with open(blueprint_file) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    _is_created(blueprint_file_location, yml["bags"])

    # Cleanup
    tmp_blueprint_file = blueprint_folder/"blueprint.yml"
    os.rename(blueprint_file, tmp_blueprint_file)
    shutil.rmtree(blueprint_file_location)
    os.makedirs(blueprint_file_location)
    os.rename(tmp_blueprint_file, blueprint_file)


def _is_created(context: Path, yml: Dict[str, Any]):

    assert context.is_dir()
    assert (context/BAG_FILE).is_file()

    for bag, properties in yml.items():
        if "bags" in properties:
            _is_created(context/bag, properties["bags"])
