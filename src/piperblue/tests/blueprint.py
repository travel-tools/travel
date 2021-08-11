import os
import sys
from pathlib import Path

from piperblueexample.blueprint import PiperBlueprintExample


if __name__ == '__main__':

    resources_folder = str(Path(sys.modules[PiperBlueprintExample.__module__].__file__).parent / "resources")

    context = "blueprint"

    yml = {
        "package": {
            "name": "blueprint",
            "description": "bla"
        },
        "python": "3.7.4"
    }

    PiperBlueprintExample(resources_folder, context, yml)

    # Assertions
    assert os.path.isdir(context)
    package = os.path.join(context, "package")
    assert os.path.isdir(os.path.join(package, "blueprint"))
    with open(os.path.join(package, "setup.py")) as f:
        assert "3.7.4" in f.read()
