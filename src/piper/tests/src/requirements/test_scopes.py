from pathlib import Path

from piper.custom.scopes.scoped_venvs import ScopedVirtualenvs


def test_scopes(complex_project):

    # Pipe
    pipe = complex_project.pipes[complex_project.first]

    # Create all scopes
    scopes = ScopedVirtualenvs(pipe, touch_requirements_file=True)
    scopes.create_all()
    scopes.update_all()
    scopes.freeze_all()

    # Verify envs
    for scope in scopes.envs.keys():
        assert (Path(pipe.location)/f"venv-{pipe.name}-{scope}").is_dir()

    # Check for single env
    for scope, env in scopes.envs.items():

        # Read the requirements file
        with open(env.requirements_file, "r") as f:
            requirements = f.read()

        # Are there the extra requirements?
        for req in pipe.scopes[scope].requirements:
            assert req in requirements

        # Are there the pipe requirements?
        for req in pipe.requirements:
            assert req in requirements
