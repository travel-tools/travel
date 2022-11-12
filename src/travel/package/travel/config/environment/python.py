import logging

from travel.config.environment.configuration import travel_config
from travel.config.project import Project
from travel.tools.python import Python, main_python

logger = logging.getLogger(__name__)


def get_right_python(project: Project) -> Python:

    # Get the desired version of python for this project from the global travel config
    desired_version = project.root.python
    python_path = travel_config.python.get(desired_version, None)

    # If not configured, check compatibility
    if not python_path:

        logger.warning(f"You do not have a Python {desired_version} configured in your global travel config file.")
        version = main_python.run("--version", capture=True).stdout
        if desired_version not in version:
            raise AssertionError(f"Your travel python is not compatible with this project, "
                                 f"that requires {desired_version}. Install Python {desired_version} on your machine, "
                                 f"get its <path> and configure travel to use it with "
                                 f"'travel config add python {desired_version} <path>'")
        else:
            logger.info("Your travel python is compatible with this project.")
            venv_python = main_python

    else:

        # Check the pointed python version
        venv_python = Python(path=python_path)
        version = venv_python.run("--version", capture=True).stdout.replace("[\n\r]+", "")
        if desired_version not in version:
            raise AssertionError(f"The python pointed by {desired_version} in your travel config file "
                                 f"is actually a {version} ({python_path}). Fix the pointer.")

    return venv_python
