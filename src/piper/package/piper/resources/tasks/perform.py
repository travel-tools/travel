import argparse
import importlib
import inspect
import os
import re
from pathlib import Path

import yaml
from typing import Dict, Any
from pipertask.task import PiperTask


def _read_config(context: str, name: str) -> (Dict[str, Any], str):
    # Read the pipe file
    with open(os.path.join(context, "pipe.yml")) as p:
        pipe = yaml.load(p, Loader=yaml.SafeLoader) or {}

    # Get all the tasks with matching name
    matching = [
        task
        for step in pipe.get("tasks", {}).values()
        for tasks in step.values()
        for task in tasks
        if task.get("name") == name
    ]
    if len(matching) != 1:
        raise ValueError(f"There should be a single task named {name}")

    # Get package name
    package = re.search(r"^([a-zA-Z0-9\-\._]+)", matching[0]["pipertask"]).group(1)

    # Return the config
    return matching[0].get("config", {}), package


def perform(context, name):

    # Get configs
    config, package = _read_config(context, name)

    # Import the task class
    module = f"{package}.task"
    all_tasks = inspect.getmembers(
        importlib.import_module(module),
        lambda member: inspect.isclass(member) and member.__module__ == module and issubclass(member, PiperTask)
    )[0]
    task = all_tasks[1]

    # Perform the task
    print(f"   TASK {name}   ".center(60, '*'))
    task().perform(Path(context), config)
    print("*"*60)


def main():

    # Parse
    parser = argparse.ArgumentParser()
    parser.add_argument("--context")
    parser.add_argument("--task")
    args = parser.parse_args()

    perform(args.context, args.task)


if __name__ == '__main__':

    main()
