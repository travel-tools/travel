import logging
import os

from piper.config.sanitizers import python_sanitizer, pip_sanitizer

logger = logging.getLogger(__name__)


class Pipe:

    def __init__(self, location: str, yml: dict):
        self.location = location
        self.name = os.path.basename(os.path.normpath(location))
        self.group = []

        # Pop the config entries
        config = yml.copy()
        self.python = python_sanitizer.sanitize_version(config.pop("python", None), nullable=True)
        self.dependencies = {pip_sanitizer.sanitize_package(dep): None for dep in config.pop("dependencies", [])}
        self.requirements = {pip_sanitizer.sanitize_package(name): pip_sanitizer.sanitize_version(version) for name, version in config.pop("requirements", {}).items()}

        # Extra utils
        self.package = self.name  # But could be different
        self.setup_py_folder = os.path.join(self.location, "package")  # But could be different
        self.build_folder = os.path.join(self.location, "build")  # But could be different
        self.requirements_file = os.path.join(self.setup_py_folder, "requirements.txt")

        # If there are still configs, they are unknown. Raise an error
        if config:
            raise KeyError(f"Unknown configuration in pipe file: {config}")

    def fill_dependency_with_pipe(self, pipe):
        self.dependencies[pipe.name] = pipe

    def flat_dependencies(self, with_current: bool = False):

        def visit(pipe, visited, level=0):
            for dep in pipe.dependencies.values():
                visited[dep] = max(level, visited.get(dep, level))
                visit(dep, visited, level=level+1)
            return visited

        pipes = visit(self, {})
        dependencies = [pipe for pipe, level in sorted(pipes.items(), key=lambda x: x[1], reverse=True)]
        if with_current:
            dependencies.append(self)
        return dependencies

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(self)
