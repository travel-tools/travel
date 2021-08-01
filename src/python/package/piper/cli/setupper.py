import os
from pathlib import Path
from typing import Set

from piper.config.pipe import Pipe
from piper.config.reader import get_pipe_name, read_all_pipes
from piper.tools.python import main_python
from piper.tools.venv import Virtualenv


def _setup(pipe: Pipe):

    # Prepare the requirements file
    if not os.path.isfile(pipe.requirements_file):
        Path(pipe.requirements_file).touch()

    # Create the virtualenv
    venv = Virtualenv(main_python=main_python, pipe=pipe)
    venv.create()

    # Pip freeze
    venv.freeze()


def _setup_from_pipe(pipe: Pipe, done: Set[Pipe]):

    if not pipe.group:

        # Setup dependencies first, then the pipe
        for p in [*pipe.flat_dependencies(), pipe]:
            if p not in done:
                _setup(p)
                done.add(p)

    else:

        # Setup each element of the group
        for pipe in pipe.group:
            _setup_from_pipe(pipe, done=done)


def setup_from_pipe(pipe: Pipe):
    _setup_from_pipe(pipe, done=set())


def setup(pipe_location: str):

    # Read the target pipe and all the pipes
    target = get_pipe_name(pipe_location)
    pipes = read_all_pipes(pipe_location)

    # Setup this target pipe
    setup_from_pipe(pipes[target])
