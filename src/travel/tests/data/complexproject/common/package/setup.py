from setuptools import setup, find_packages
import os


# Read requirements
requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()


# Package configuration
setup(name="common",
      version="0.0.0",
      description="A common package",
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements)
