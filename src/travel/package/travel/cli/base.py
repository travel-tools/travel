import abc
import logging
from typing import Set, List

from travel.config.bag import Bag
from travel.config.project import Project
from travel.config.reader import parse_bags
from travel.custom.tasks import performer

logger = logging.getLogger(__name__)


class TravelCommand(abc.ABC):

    @abc.abstractmethod
    def _phase_name(self) -> str:
        pass

    def _perform_tasks(self, bag: Bag, project: Project, step: str) -> bool:
        return performer.perform_tasks(self._phase_name(), step, bag)

    @abc.abstractmethod
    def _manage(self, bag: Bag, project: Project):
        pass

    def _manage_from_bag_recursive(self, bag: Bag, project: Project, done: Set[Bag]):

        if not bag.group:

            # Manage dependencies first, then the bag
            for b in [*bag.flat_dependencies(), bag]:
                if b not in done:
                    logger.info("")
                    logger.info("="*60)
                    logger.info(f"=== {b.name.center(52, ' ')} ===")
                    logger.info("="*60)
                    self._perform_tasks(b, project, "pre")
                    if not self._perform_tasks(b, project, "instead"):
                        self._manage(b, project)
                    self._perform_tasks(b, project, "post")
                    logger.info("=" * 60)
                    logger.info("")
                    logger.info("")
                    done.add(b)

        else:

            # Manage each element of the group
            for bag in bag.group:
                self._manage_from_bag_recursive(bag, project, done=done)

    def manage_from_bag(self, bag: Bag, project: Project):
        self._manage_from_bag_recursive(bag, project, done=set())

    def manage(self, context: str, target: str = None) -> (Bag, List[Bag]):

        # Read the entire project
        project = Project(context)
        bag, bags = parse_bags(context, target=target, bags=project.bags)

        # Perform the action
        self.manage_from_bag(bag, project)
        return bag, bags
