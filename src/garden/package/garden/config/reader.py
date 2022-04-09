import logging
import os
from pathlib import Path
from typing import List, Dict

import yaml
from garden.config.nest import Nest

NEST_FILE = "nest.yml"


logger = logging.getLogger(__name__)


def _read_nest(location: str) -> Nest:

    # Read the nest file
    path = os.path.join(location, NEST_FILE)
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
        return Nest(location=location, yml=yml)


def _has_nest(location: str) -> bool:
    return os.path.isfile(os.path.join(location, NEST_FILE))


def get_nest_name(location: str) -> str:
    return os.path.basename(os.path.normpath(location))


def read_all_nests(location: str) -> Dict[str, Nest]:

    # Find the uppermost (parent) nest file
    uppermost = location
    while _has_nest(location):
        uppermost = location
        location = str(Path(location).parent)

    # Read main nest file and nested nest files
    nests = {nest.name: nest for nest in _read_nests_from(uppermost)}
    # Set the root context
    for n in nests.values():
        n.root_context = uppermost

    # Build dependencies
    for name in nests:
        for nest in nests.values():
            if name in nest.dependencies:
                nest.fill_dependency_with_nest(nests[name])
    return nests


def parse_nests(location: str, target: str = None) -> (Nest, Nest):

    # Read the target nest and all the nests
    target = target or get_nest_name(location)
    nests = read_all_nests(location)

    # Manage this target nest
    if target not in nests:
        raise ValueError(f"The specified nest \"{target}\" does not exist in {location}")
    nest = nests[target]
    return nest, nests


def _read_nests_from(location: str) -> List[Nest]:

    # Read the local nest
    group = []
    nest = _read_nest(location)

    # Read all nests recursively
    nests = [nest]
    for directory in os.listdir(location):
        current = os.path.join(location, directory)
        if _has_nest(current):
            children = _read_nests_from(current)
            group = group + children
            nests = nests + children

    # Set the nested group
    nest.group = group
    return nests
