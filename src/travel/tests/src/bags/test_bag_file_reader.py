def test_finder(complex_project):
    # Number of bags
    bags = complex_project.bags
    assert len(bags) == 7
    assert len([
        b for b in bags.keys()
        if b in [
            complex_project.name, 
            complex_project.common, 
            complex_project.tasks, 
            complex_project.microservices, 
            complex_project.first, 
            complex_project.second, 
            complex_project.traveltask_example
        ]
    ]) == 7


def test_structure(complex_project):
    bags = complex_project.bags
    # Root context
    assert len([b for b in bags.values() if b.root_context != complex_project.travel_project]) == 0
    # Dependencies
    assert bags[complex_project.second].flat_dependencies(with_current=True) == [
        bags[complex_project.common],
        bags[complex_project.first],
        bags[complex_project.second]
    ]


def test_read_tasks(complex_project):
    # Tasks reader
    bags = complex_project.bags
    assert len(bags[complex_project.first].tasks["setup"]["pre"]) == 2
