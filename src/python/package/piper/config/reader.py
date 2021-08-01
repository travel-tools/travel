import logging
import os
from pathlib import Path
from typing import List

import yaml
from piper.config.pipe import Pipe

_PIPE_FILE = "pipe.yml"


logger = logging.getLogger(__name__)


def read_pipe(location: str) -> Pipe:

    # Read the pipe file
    path = os.path.join(location, _PIPE_FILE)
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
        return Pipe(location=location, yml=yml)


def _has_pipe(location: str) -> bool:
    return os.path.isfile(os.path.join(location, _PIPE_FILE))


def read_pipe_files(location: str) -> List[Pipe]:

    # Find the uppermost (parent) pipe file
    uppermost = location
    while _has_pipe(location):
        uppermost = location
        location = str(Path(location).parent)

    # Read main pipe file and nested pipe files
    return [read_pipe(uppermost)] + _read_pipe_files_from(uppermost)


def _read_pipe_files_from(location: str) -> List[Pipe]:

    # Read all pipes recursively
    pipes = []
    for directory in os.listdir(location):
        try:
            current = os.path.join(location, directory)
            pipes.append(read_pipe(current))
            pipes = pipes + _read_pipe_files_from(current)
        except FileNotFoundError:
            pass
    return pipes
