import os
import sys
from pathlib import Path

from piperblueexample.blueprint import PiperBlueprintExample


def test_generation():

    # Parameters
    resources_folder = str(Path(sys.modules[PiperBlueprintExample.__module__].__file__).parent / "resources")
    context = "example"
    name = "thename"
    description = "blabla"
    version = "3.7.4"
    yml = {
        "package": {
            "name": name,
            "description": description
        },
        "python": version
    }

    # Generate
    PiperBlueprintExample().generate(resources_folder, context, yml)

    # Folders created and renamed
    assert os.path.isdir(context)
    package_folder = os.path.join(context, "package")
    assert os.path.isdir(os.path.join(package_folder, name))

    # Placeholders substituted
    with open(os.path.join(package_folder, "setup.py")) as f:
        assert f'description="{description}"' in f.read()
    with open(os.path.join(context, "pipe.yml")) as f:
        assert version in f.read()
