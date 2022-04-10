from pathlib import Path

from travel.custom.scopes.scoped_venvs import ScopedVirtualenvs


def test_scopes(complex_project):

    # Bag
    bag = complex_project.bags[complex_project.first]

    # Create all scopes
    scopes = ScopedVirtualenvs(bag, touch_requirements_file=True)
    scopes.create_all()
    scopes.update_all()
    scopes.freeze_all()

    # Verify envs
    for scope in scopes.envs.keys():
        assert (Path(bag.location)/f"venv-{bag.name}-{scope}").is_dir()

    # Check for single env
    for scope, env in scopes.envs.items():

        # Read the requirements file
        with open(env.requirements_file, "r") as f:
            requirements = f.read()

        # Are there the extra requirements?
        for req in bag.scopes[scope].requirements:
            assert req in requirements

        # Are there the bag requirements?
        for req in bag.requirements:
            assert req in requirements
