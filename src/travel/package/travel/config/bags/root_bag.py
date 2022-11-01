from travel.config.bags.base_bag import BaseBag
from travel.config.sanitizers import python_sanitizer
from travel.config.subconfigs.pip import PipConfig


class RootBag(BaseBag):

    def __init__(self, location: str, yml: dict, root_context: str = None):
        super().__init__(location, root_context)

        # Pop the config entries
        config = yml.copy()
        self.python = python_sanitizer.sanitize_version(config.pop("python", None), nullable=True)
        self.pip = PipConfig(config.pop("pip", {}))
