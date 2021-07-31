import os


class Pipe:

    def __init__(self, location: str, yml: dict):
        self.location = location
        self.name = os.path.basename(os.path.normpath(location))

        # Pop the config entries  # TODO sanity checks! Because we will execute scripts
        config = yml.copy()
        self.python = config.pop("python", None)
        self.dependencies = config.pop("dependencies", [])
        self.requirements = config.pop("requirements", {})

        # If there are still configs, they are unknown. Raise an error
        if config:
            raise KeyError(f"Unkown configuration in pipe file: {config}")

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(self)
