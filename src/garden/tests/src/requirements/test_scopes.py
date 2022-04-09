from pathlib import Path

from garden.custom.scopes.scoped_venvs import ScopedVirtualenvs


def test_scopes(complex_project):

    # Nest
    nest = complex_project.nests[complex_project.first]

    # Create all scopes
    scopes = ScopedVirtualenvs(nest, touch_requirements_file=True)
    scopes.create_all()
    scopes.update_all()
    scopes.freeze_all()

    # Verify envs
    for scope in scopes.envs.keys():
        assert (Path(nest.location)/f"venv-{nest.name}-{scope}").is_dir()

    # Check for single env
    for scope, env in scopes.envs.items():

        # Read the requirements file
        with open(env.requirements_file, "r") as f:
            requirements = f.read()

        # Are there the extra requirements?
        for req in nest.scopes[scope].requirements:
            assert req in requirements

        # Are there the nest requirements?
        for req in nest.requirements:
            assert req in requirements
