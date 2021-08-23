from piper.config.sanitizers.name_sanitizer import sanitize_name
from piper.config.sanitizers.pip_sanitizer import sanitize_package_with_version


class Task:

    def __init__(self, yml):
        self.pipertask = sanitize_package_with_version(yml.pop("pipertask"))
        self.name = sanitize_name(yml.pop("name"))
        self.config = yml.pop("config", {})

        self.pipertask_name, self.pipertask_version = self.pipertask.split("==")

        # If there are still configs, they are unknown. Raise an error
        if yml:
            raise KeyError(f"Unknown configuration in pipe file, task {self.name}: {yml}")
