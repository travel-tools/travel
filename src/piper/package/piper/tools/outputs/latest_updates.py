import yaml


class LatestUpdate:

    def __init__(self, config):
        self.requirements = config.pop("requirements")
        self.dependencies = config.pop("dependencies")

    @classmethod
    def create(cls, requirements, dependencies):
        return cls({
            "requirements": requirements,
            "dependencies": dependencies
        })

    @classmethod
    def read(cls, path):
        with open(path, "r") as f:
            yml = yaml.load(f, yaml.SafeLoader) or {}
        return cls(yml)

    def write(self, path):
        with open(path, "w") as f:
            yaml.dump(vars(self), f)
