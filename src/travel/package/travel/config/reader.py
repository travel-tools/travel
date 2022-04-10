import logging
import os
from pathlib import Path
from typing import List, Dict

import yaml
from travel.config.bag import Bag

BAG_FILE = "bag.yml"


logger = logging.getLogger(__name__)


def _read_bag(location: str) -> Bag:

    # Read the bag file
    path = os.path.join(location, BAG_FILE)
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
        return Bag(location=location, yml=yml)


def _has_bag(location: str) -> bool:
    return os.path.isfile(os.path.join(location, BAG_FILE))


def get_bag_name(location: str) -> str:
    return os.path.basename(os.path.normpath(location))


def read_all_bags(location: str) -> Dict[str, Bag]:

    # Find the uppermost (parent) bag file
    uppermost = location
    while _has_bag(location):
        uppermost = location
        location = str(Path(location).parent)

    # Read main bag file and baged bag files
    bags = {bag.name: bag for bag in _read_bags_from(uppermost)}
    # Set the root context
    for b in bags.values():
        b.root_context = uppermost

    # Build dependencies
    for name in bags:
        for bag in bags.values():
            if name in bag.dependencies:
                bag.fill_dependency_with_bag(bags[name])
    return bags


def parse_bags(location: str, target: str = None) -> (Bag, Bag):

    # Read the target bag and all the bags
    target = target or get_bag_name(location)
    bags = read_all_bags(location)

    # Manage this target bag
    if target not in bags:
        raise ValueError(f"The specified bag \"{target}\" does not exist in {location}")
    bag = bags[target]
    return bag, bags


def _read_bags_from(location: str) -> List[Bag]:

    # Read the local bag
    group = []
    bag = _read_bag(location)

    # Read all bags recursively
    bags = [bag]
    for directory in os.listdir(location):
        current = os.path.join(location, directory)
        if _has_bag(current):
            children = _read_bags_from(current)
            group = group + children
            bags = bags + children

    # Set the baged group
    bag.group = group
    return bags
