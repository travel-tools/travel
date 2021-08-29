import pytest


class ComplexProject:

    def __init__(self):
        self.name = "complexproject"
        self.common = "common"
        self.tasks = "tasks"
        self.microservices = "microservices"
        self.first = "first"
        self.second = "second"
        self.pipertask_example = "pipertaskexample"

        self.piper_project = os.path.join(pytest.data, self.name)


def pytest_configure():

    pytest.data = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

    pytest.complex_project = ComplexProject()

