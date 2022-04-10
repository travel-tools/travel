import os
from pathlib import Path

from travel.cli.cleaner import Cleaner
from travel.config.sanitizers.pip_sanitizer import LATEST_PIP
from travel.tools.base_venv import LATEST_UPDATE
from travel.tools.outputs.latest_updates import LatestUpdate
from travel.tools.venv import Virtualenv


def test_quick_setup(complex_project):

    # Bag
    bag = complex_project.bags[complex_project.common]

    # Create the virtualenv
    venv = Virtualenv(bag)
    venv.create()
    venv.update()

    # Test that no update will be performed on another update
    assert venv.update() is False

    # Test that update will be performed first, and then no more
    bag.requirements = []
    assert venv.update() is True
    venv.freeze()
    assert venv.update() is False

    # Test update in case of venv mismatch
    venv.pip.install("jsonargon==0.1.1")
    assert venv.update() is True
    assert venv.update() is False

    # Remove the file
    latest_update_path = Path(venv.path)/LATEST_UPDATE
    os.remove(latest_update_path)
    assert venv.update() is True
    assert venv.update() is False

    # Test update in case of dependencies mismatch (simulate a change on filesystem)
    update = LatestUpdate.read(latest_update_path)
    update.dependencies = ["fake"]
    update.write(latest_update_path)
    assert venv.update() is True
    assert venv.update() is False


def test_pip_version(complex_project):

    # Bag
    bag = complex_project.bags[complex_project.common]

    # Create the virtualenv
    venv = Virtualenv(bag)
    venv.create()
    venv.update()

    # Check pip version
    assert bag.pip.version in venv.pip.run("--version", capture=True).stdout

    # Force pip version to latest
    old_pip_version = bag.pip.version
    bag.pip.version = LATEST_PIP

    # Update pip and check if the old version is no more there
    venv.update()
    assert old_pip_version not in venv.pip.run("--version", capture=True).stdout


def test_remove_requirements(complex_project):

    # Common bag
    bag = complex_project.bags[complex_project.common]

    # Create the virtualenv
    venv = Virtualenv(bag)
    venv.create()
    venv.update()

    # Check the requirement file
    venv.freeze()
    with open(bag.requirements_file, "r") as f:
        right_requirements = f.read()

    # Install manually a requirement
    venv.pip.run("install pandas")

    # Check that this function removes the manually inserted requirements
    venv.update()
    venv.freeze()
    with open(bag.requirements_file, "r") as f:
        now_requirements = f.read()
    assert right_requirements == now_requirements

    # Remove requirements from the bag
    old_requirements = bag.requirements
    bag.requirements = ["pandas==1.3.3"]
    venv.update()
    venv.freeze()
    with open(bag.requirements_file, "r") as f:
        now_requirements = f.read()
    assert "pandas" in now_requirements
    assert "python-dateutil" in now_requirements
    assert "six" in now_requirements
    for r in old_requirements:
        assert r not in now_requirements

    # Clean everything
    Cleaner().manage_from_bag(bag)
    os.remove(bag.requirements_file)

