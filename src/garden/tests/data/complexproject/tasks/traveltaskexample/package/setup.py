from setuptools import setup, find_packages
import os


# Function to retrieve resources files
def _get_resources(package_name):
    # Get all the resources (also on baged levels)
    res_paths = os.path.join(package_name, "resources")
    all_resources = [os.path.join(folder, file) for folder, _, files in os.walk(res_paths) for file in files]
    # Remove the prefix: start just from "resources"
    return [resource[resource.index("resources"):] for resource in all_resources]


# Read requirements
this_location = os.path.dirname(os.path.realpath(__file__))
requirements_file = os.path.join(this_location, "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()


# Package configuration
setup(
    name="traveltaskexample",
    version="0.0.0",
    description="An example of Travel Task",
    packages=find_packages(),
    package_data={"traveltaskexample": _get_resources("traveltaskexample")},
    install_requires=requirements
)
