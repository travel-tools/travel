import os
from pathlib import Path

import yaml
from piper.config.pipe import Pipe

_PIPE_FILE = "pipe.yml"


def _read_pipe(location: str) -> Pipe:

    # Read the pipe file
    path = os.path.join(location, _PIPE_FILE)
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
        return Pipe(location=location, yml=yml)


def read_pipe_files(location: str):

    # Read all pipes
    pipes = [
        _read_pipe(os.path.join(*path.parts[:-1])) for path in Path(location).rglob(_PIPE_FILE)
        # # Only if there is a previous pipe file in the upper folder (if you comment it, read the main one too)
        #if os.path.isfile(os.path.join(*path.parts[:-2], _PIPEFILE))
    ]
    return pipes
