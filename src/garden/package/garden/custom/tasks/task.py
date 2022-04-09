from garden.config.sanitizers.name_sanitizer import sanitize_name
from garden.config.sanitizers.pip_sanitizer import sanitize_versioned_package


class Task:

    def __init__(self, yml):
        self.gardentask = sanitize_versioned_package(yml.pop("gardentask"))
        self.name = sanitize_name(yml.pop("name"))
        self.config = yml.pop("config", {})

        # If there are still configs, they are unknown. Raise an error
        if yml:
            raise KeyError(f"Unknown configuration in pipe file, task {self.name}: {yml}")