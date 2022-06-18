from traveltask_example.config import TaskConfig


def perform(config: TaskConfig):

    print(f"Task: {config.task} for {config.context}")

    print(f"Parameter: {config.something}")
    print(f"Parameter: {config.number}")
