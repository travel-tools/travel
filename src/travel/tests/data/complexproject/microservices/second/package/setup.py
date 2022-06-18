import os
from setuptools import setup, find_packages


# Read requirements
requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()


# Package configuration
setup(name="second",
      version="0.0.0",
      description="A second package",
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements)
