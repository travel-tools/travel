import os

import pytest
from garden.config.reader import read_all_pipes


class ComplexProject:

    def __init__(self, data_location):
        self.name = "complexproject"
        self.common = "common"
        self.tasks = "tasks"
        self.microservices = "microservices"
        self.first = "first"
        self.second = "second"
        self.gardentask_example = "gardentaskexample"

        self.garden_project = os.path.join(data_location, self.name)
        self.pipes = read_all_pipes(self.garden_project)


@pytest.fixture
def data_location():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.fixture
def complex_project(data_location):
    return ComplexProject(data_location)
