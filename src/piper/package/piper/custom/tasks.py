import os

from piper import RESOURCES_LOCATION
from piper.config.pipe import Pipe
from piper.config.sanitizers.name_sanitizer import sanitize_name
from piper.config.sanitizers.pip_sanitizer import sanitize_package_with_version
from piper.tools.venv import Virtualenv


_PERFORM_TASK = os.path.join(RESOURCES_LOCATION, "tasks", "task.py")


class Task:

    def __init__(self, yml):
        self.task = sanitize_package_with_version(yml.pop("task"))
        self.name = sanitize_name(yml.pop("name"))
        self.config = yml.pop("config", {})


def perform_tasks(phase: str, step: str, pipe: Pipe):

    # Get tasks
    tasks = pipe.tasks.get(phase, {}).get(step, {})
    if tasks:

        # Create the env for tasks # TODO could be different venvs to avoid conflicts?
        venv = Virtualenv(Pipe(location=pipe.tasks_folder, yml={}))
        venv.create()
        venv.pip.install(tasks, allow_local_files=True)

        # Perform each task in order
        for task in tasks:
            venv.python.run(f"{_PERFORM_TASK} --context {pipe.location} --task {task.name}")
