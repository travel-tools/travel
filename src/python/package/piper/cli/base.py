import abc
from typing import Set

from piper.config.pipe import Pipe
from piper.config.reader import get_pipe_name, read_all_pipes
from piper.tools.python import main_python, Python


class PiperCommand(abc.ABC):

    def __init__(self, python: Python = main_python):
        self.main_python = python

    @abc.abstractmethod
    def _manage(self, pipe: Pipe):
        pass

    def _manage_from_pipe_recursive(self, pipe: Pipe, done: Set[Pipe]):

        if not pipe.group:

            # Manage dependencies first, then the pipe
            for p in [*pipe.flat_dependencies(), pipe]:
                if p not in done:
                    self._manage(p)
                    done.add(p)

        else:

            # Manage each element of the group
            for pipe in pipe.group:
                self._manage_from_pipe_recursive(pipe, done=done)

    def manage_from_pipe(self, pipe: Pipe):
        self._manage_from_pipe_recursive(pipe, done=set())

    def manage(self, pipe_location: str):

        # Read the target pipe and all the pipes
        target = get_pipe_name(pipe_location)
        pipes = read_all_pipes(pipe_location)

        # Manage this target pipe
        self.manage_from_pipe(pipes[target])