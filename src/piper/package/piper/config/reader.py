import logging
import os
from pathlib import Path
from typing import List, Dict

import yaml
from piper.config.pipe import Pipe

PIPE_FILE = "pipe.yml"


logger = logging.getLogger(__name__)


def _read_pipe(location: str) -> Pipe:

    # Read the pipe file
    path = os.path.join(location, PIPE_FILE)
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
        return Pipe(location=location, yml=yml)


def _has_pipe(location: str) -> bool:
    return os.path.isfile(os.path.join(location, PIPE_FILE))


def get_pipe_name(location: str) -> str:
    return os.path.basename(os.path.normpath(location))


def read_all_pipes(location: str) -> Dict[str, Pipe]:

    # Find the uppermost (parent) pipe file
    uppermost = location
    while _has_pipe(location):
        uppermost = location
        location = str(Path(location).parent)

    # Read main pipe file and nested pipe files
    pipes = {pipe.name: pipe for pipe in _read_pipes_from(uppermost)}
    # Set the root context
    for p in pipes.values():
        p.root_context = uppermost

    # Build dependencies
    for name in pipes:
        for pipe in pipes.values():
            if name in pipe.dependencies:
                pipe.fill_dependency_with_pipe(pipes[name])
    return pipes


def _read_pipes_from(location: str) -> List[Pipe]:

    # Read the local pipe
    group = []
    pipe = _read_pipe(location)

    # Read all pipes recursively
    pipes = [pipe]
    for directory in os.listdir(location):
        current = os.path.join(location, directory)
        if _has_pipe(current):
            children = _read_pipes_from(current)
            group = group + children
            pipes = pipes + children

    # Set the nested group
    pipe.group = group
    return pipes
