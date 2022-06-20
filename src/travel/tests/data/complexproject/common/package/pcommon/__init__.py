import os

PACKAGE_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)))
RESOURCES_LOCATION = os.path.join(PACKAGE_LOCATION, "resources")
NESTED_LOCATION = os.path.join(RESOURCES_LOCATION, "nested")


# Just to test that the file exists
with open(os.path.join(NESTED_LOCATION, "config.yml"), "r") as f:
    f.read()
