def test_finder(complex_project):
    # Number of nests
    nests = complex_project.nests
    assert len(nests) == 7
    assert len([
        n for n in nests.keys()
        if n in [
            complex_project.name, 
            complex_project.common, 
            complex_project.tasks, 
            complex_project.microservices, 
            complex_project.first, 
            complex_project.second, 
            complex_project.gardentask_example
        ]
    ]) == 7


def test_structure(complex_project):
    nests = complex_project.nests
    # Root context
    assert len([n for n in nests.values() if n.root_context != complex_project.garden_project]) == 0
    # Dependencies
    assert nests[complex_project.second].flat_dependencies(with_current=True) == [
        nests[complex_project.common],
        nests[complex_project.first],
        nests[complex_project.second]
    ]


def test_read_tasks(complex_project):
    # Tasks reader
    nests = complex_project.nests
    assert len(nests[complex_project.first].tasks["setup"]["pre"]) == 2
