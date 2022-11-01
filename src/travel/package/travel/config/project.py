from travel.config.reader import parse_bags, find_root_bag_location


class Project:

    def __init__(self, location: str):
        uppermost = find_root_bag_location(location)
        self.root, self.bags = parse_bags(uppermost)

        if not self.root.python:
            raise ValueError(f"You need to configure the python version in the root bag.yml ({self.root.location}), e.g. python: 3.7.4")
