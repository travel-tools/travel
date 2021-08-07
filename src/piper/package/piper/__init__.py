import logging
import sys

import os

PACKAGE_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)))
RESOURCES_LOCATION = os.path.join(PACKAGE_LOCATION, "resources")
CONFIG_LOCATION = os.path.join(RESOURCES_LOCATION, "config")


def _init_logger():
    root_log = logging.getLogger()
    formatter = logging.Formatter("%(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root_log.addHandler(stream_handler)
    root_log.setLevel(logging.INFO)


_init_logger()
