import os
import shutil
from pathlib import Path

from travel.cli import adder


def test_add(data_location):

    # Add a bag
    adder.run(
        data_location,
        "gh:travel-tools/cookiecutter-travelplan",
        no_input=True,
        config=["name=ok"]
    )

    # Check creation
    output_folder = os.path.join(data_location, "ok")
    assert Path(output_folder).is_dir()

    # Cleanup
    shutil.rmtree(output_folder)
