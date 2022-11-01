import os


class BaseBag:

    def __init__(self, location: str, root_context: str = None):
        self.location = location
        self.root_context = root_context
        self.name = os.path.basename(os.path.normpath(location))
        self.group = []

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(self)
