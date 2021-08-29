from piper.config.reader import read_all_pipes


def _read(complex_project):
    return read_all_pipes(complex_project.piper_project)


def test_finder(complex_project):
    # Number of pipes
    pipes = _read(complex_project)
    assert len(pipes) == 7
    assert len([
        p for p in pipes.keys() 
        if p in [
            complex_project.name, 
            complex_project.common, 
            complex_project.tasks, 
            complex_project.microservices, 
            complex_project.first, 
            complex_project.second, 
            complex_project.pipertask_example
        ]
    ]) == 7


def test_structure(complex_project):
    pipes = _read(complex_project)
    # Root context
    assert len([p for p in pipes.values() if p.root_context != complex_project.piper_project]) == 0
    # Dependencies
    assert pipes[complex_project.second].flat_dependencies(with_current=True) == [
        pipes[complex_project.common],
        pipes[complex_project.first],
        pipes[complex_project.second]
    ]


def test_read_tasks(complex_project):
    # Tasks reader
    pipes = _read(complex_project)
    assert len(pipes[complex_project.first].tasks["setup"]["pre"]) == 2
