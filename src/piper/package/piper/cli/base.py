import abc
import logging
from typing import Set

from piper.config.pipe import Pipe
from piper.config.reader import get_pipe_name, read_all_pipes
from piper.tools.python import main_python, Python


logger = logging.getLogger(__name__)


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
                    logger.info("")
                    logger.info("="*60)
                    logger.info(f"=== {p.name.center(52, ' ')} ===")
                    logger.info("="*60)
                    self._manage(p)
                    logger.info("=" * 60)
                    logger.info("")
                    logger.info("")
                    done.add(p)

        else:

            # Manage each element of the group
            for pipe in pipe.group:
                self._manage_from_pipe_recursive(pipe, done=done)

    def manage_from_pipe(self, pipe: Pipe):
        self._manage_from_pipe_recursive(pipe, done=set())

    def manage(self, context: str, package: str = None) -> (Pipe, Pipe):

        # Read the target pipe and all the pipes
        target = package or get_pipe_name(context)
        pipes = read_all_pipes(context)

        # Manage this target pipe
        if target not in pipes:
            raise ValueError(f"The specified pipe does not exist: {context}")
        pipe = pipes[target]
        self.manage_from_pipe(pipe)
        return pipe, pipes
