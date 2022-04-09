import abc
import logging
from typing import Set

from garden.config.pipe import Pipe
from garden.config.reader import get_pipe_name, read_all_pipes, parse_pipes
from garden.custom.tasks import performer
from garden.tools.python import main_python, Python

logger = logging.getLogger(__name__)


class GardenCommand(abc.ABC):

    def __init__(self, python: Python = main_python):
        self.main_python = python

    @abc.abstractmethod
    def _phase_name(self) -> str:
        pass

    def _perform_tasks(self, pipe: Pipe, step: str):
        return performer.perform_tasks(self._phase_name(), step, pipe)

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
                    self._perform_tasks(p, "pre")
                    self._manage(p)
                    self._perform_tasks(p, "post")
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

    def manage(self, context: str, target: str = None) -> (Pipe, Pipe):
        pipe, pipes = parse_pipes(context, target)
        self.manage_from_pipe(pipe)
        return pipe, pipes