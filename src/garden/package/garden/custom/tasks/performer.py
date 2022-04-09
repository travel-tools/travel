import logging
import os

import pkg_resources
from garden import RESOURCES_LOCATION
from garden.config.nest import Nest
from garden.config.sanitizers import pip_sanitizer
from garden.tools.venv import Virtualenv

_PERFORM_TASK = os.path.join(RESOURCES_LOCATION, "tasks", "perform.py")


logger = logging.getLogger(__name__)


def perform_tasks(phase: str, step: str, nest: Nest):

    # Get tasks
    tasks = nest.tasks.get(phase, {}).get(step, {})
    if tasks:

        # Create the env for tasks # TODO could be different venvs to avoid conflicts?
        logger.info("*"*60)
        logger.info(f"   TASKS {phase}: {step}   ".center(60, "*"))
        logger.info("*" * 60)
        venv = Virtualenv(Nest(location=nest.tasks_folder, yml={}))
        venv.create()

        # Install PyYAML for the performer
        version = pip_sanitizer.sanitize_version(pkg_resources.get_distribution("PyYAML").version)
        venv.pip.install(f"PyYAML=={version}")

        # Install the gardentasks
        venv.pip.install([t.pipertask for t in tasks], allow_nests_from=nest.root_context)

        # Perform each task in order
        for task in tasks:
            venv.python.run(f"{_PERFORM_TASK} --context {nest.location} --task {task.name}")
        logger.info(f"   END TASKS {phase}: {step}   ".center(60, "*"))
        logger.info("*"*60)
