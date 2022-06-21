import logging
import os

from travel.cli.console.output import log_title
from travel.config.bag import Bag
from travel.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


def perform_tasks(phase: str, step: str, bag: Bag) -> bool:

    # Get tasks
    tasks = bag.tasks.get(phase, {}).get(step, [])
    if tasks:
        log_title(logger, f"TASKS {phase}: {step}")

    # For each task
    for task in tasks:

        # Create the env
        log_title(logger, f"{task.name}", char='-')
        task_folder = os.path.join(bag.build_folder, f"task-{task.package.split('==')[0]}")
        os.makedirs(task_folder, exist_ok=True)
        venv = Virtualenv(Bag(location=task_folder, yml={}))
        venv.create()

        # Install the package
        venv.pip.install([task.package], allow_bags_from=bag.root_context)

        # Append common args (context, task) and join the config section
        base_command = f"-m {task.python_module} --context \"{bag.location}\" --task \"{task.name}\" "
        base_command = base_command + " ".join([f"--{key} \"{value}\"" for key, value in task.config.items()])

        # Perform
        venv.python.run(base_command, cwd=bag.location)
        log_title(logger, f"END {task.name}", char='-', ending=True)

    if tasks:
        log_title(logger, f"END TASKS {phase}: {step}", ending=True)
        return True

    return False
