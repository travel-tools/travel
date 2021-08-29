import os
import pytest

from piper.config.reader import read_all_pipes


PROJECT = pytest.complex_project


def _read():
    return read_all_pipes(PROJECT.piper_project)


def test_finder():
    # Number of pipes
    pipes = _read()    
    assert len(pipes) == 7
    assert len([
        p for p in pipes.keys() 
        if p in [
            PROJECT.name, 
            PROJECT.common, 
            PROJECT.tasks, 
            PROJECT.microservices, 
            PROJECT.first, 
            PROJECT.second, 
            PROJECT.pipertask_example
        ]
    ]) == 7


def test_structure():
    pipes = _read()
    # Root context
    assert len([p for p in pipes.values() if p.root_context != PROJECT.piper_project]) == 0
    # Dependencies
    assert pipes[PROJECT.second].flat_dependencies(with_current=True) == [
        pipes[PROJECT.common],
        pipes[PROJECT.first],
        pipes[PROJECT.second]
    ]


def test_read_tasks():
    # Tasks reader
    pipes = _read()
    assert len(pipes[PROJECT.first].tasks["setup"]["pre"]) == 2
