from travel.config.sanitizers.name_sanitizer import sanitize_name
from travel.config.sanitizers.pip_sanitizer import sanitize_versioned_package


class Task:

    def __init__(self, yml):
        self.package = sanitize_versioned_package(yml.pop("task"))
        self.python_module = yml.pop("python_module", self.package.split("==")[0])
        self.name = sanitize_name(yml.pop("name"))
        self.config = yml.pop("config", {})
        for key in self.config:
            if isinstance(self.config[key], dict):
                raise ValueError(f"Task configs must not have nested dictionaries (task: {self.name}): {self.config[key]}")

        # If there are still configs, they are unknown. Raise an error
        if yml:
            raise KeyError(f"Unknown configuration in bag file, task {self.name}: {yml}")
