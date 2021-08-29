import os

from piper import RESOURCES_LOCATION
from piper.config.pipe import Pipe
from piper.tools.venv import Virtualenv

_PERFORM_TASK = os.path.join(RESOURCES_LOCATION, "tasks", "perform.py")


def perform_tasks(phase: str, step: str, pipe: Pipe):

    # Get tasks
    tasks = pipe.tasks.get(phase, {}).get(step, {})
    if tasks:

        # Create the env for tasks # TODO could be different venvs to avoid conflicts?
        venv = Virtualenv(Pipe(location=pipe.tasks_folder, yml={}))
        venv.create()
        venv.pip.install([t.pipertask for t in tasks], allow_pipes_from=pipe.root_context)

        # Perform each task in order
        for task in tasks:
            venv.python.run(f"{_PERFORM_TASK} --context {pipe.location} --task {task.name}")
