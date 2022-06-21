import abc
import logging
from typing import Set

from travel.config.bag import Bag
from travel.config.reader import parse_bags
from travel.custom.tasks import performer
from travel.tools.python import main_python, Python

logger = logging.getLogger(__name__)


class TravelCommand(abc.ABC):

    def __init__(self, python: Python = main_python):
        self.main_python = python

    @abc.abstractmethod
    def _phase_name(self) -> str:
        pass

    def _perform_tasks(self, bag: Bag, step: str) -> bool:
        return performer.perform_tasks(self._phase_name(), step, bag)

    @abc.abstractmethod
    def _manage(self, bag: Bag):
        pass

    def _manage_from_bag_recursive(self, bag: Bag, done: Set[Bag]):

        if not bag.group:

            # Manage dependencies first, then the bag
            for b in [*bag.flat_dependencies(), bag]:
                if b not in done:
                    logger.info("")
                    logger.info("="*60)
                    logger.info(f"=== {b.name.center(52, ' ')} ===")
                    logger.info("="*60)
                    self._perform_tasks(b, "pre")
                    if not self._perform_tasks(b, "instead"):
                        self._manage(b)
                    self._perform_tasks(b, "post")
                    logger.info("=" * 60)
                    logger.info("")
                    logger.info("")
                    done.add(b)

        else:

            # Manage each element of the group
            for bag in bag.group:
                self._manage_from_bag_recursive(bag, done=done)

    def manage_from_bag(self, bag: Bag):
        self._manage_from_bag_recursive(bag, done=set())

    def manage(self, context: str, target: str = None) -> (Bag, Bag):
        bag, bags = parse_bags(context, target)
        self.manage_from_bag(bag)
        return bag, bags
