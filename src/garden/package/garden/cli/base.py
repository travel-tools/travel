import abc
import logging
from typing import Set

from garden.config.nest import Nest
from garden.config.reader import get_nest_name, read_all_nests, parse_nests
from garden.custom.tasks import performer
from garden.tools.python import main_python, Python

logger = logging.getLogger(__name__)


class GardenCommand(abc.ABC):

    def __init__(self, python: Python = main_python):
        self.main_python = python

    @abc.abstractmethod
    def _phase_name(self) -> str:
        pass

    def _perform_tasks(self, nest: Nest, step: str):
        return performer.perform_tasks(self._phase_name(), step, nest)

    @abc.abstractmethod
    def _manage(self, nest: Nest):
        pass

    def _manage_from_nest_recursive(self, nest: Nest, done: Set[Nest]):

        if not nest.group:

            # Manage dependencies first, then the nest
            for n in [*nest.flat_dependencies(), nest]:
                if n not in done:
                    logger.info("")
                    logger.info("="*60)
                    logger.info(f"=== {n.name.center(52, ' ')} ===")
                    logger.info("="*60)
                    self._perform_tasks(n, "pre")
                    self._manage(n)
                    self._perform_tasks(n, "post")
                    logger.info("=" * 60)
                    logger.info("")
                    logger.info("")
                    done.add(n)

        else:

            # Manage each element of the group
            for nest in nest.group:
                self._manage_from_nest_recursive(nest, done=done)

    def manage_from_nest(self, nest: Nest):
        self._manage_from_nest_recursive(nest, done=set())

    def manage(self, context: str, target: str = None) -> (Nest, Nest):
        nest, nests = parse_nests(context, target)
        self.manage_from_nest(nest)
        return nest, nests
