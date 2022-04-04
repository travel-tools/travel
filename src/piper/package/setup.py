from setuptools import setup, find_packages
import os


# Function to retrieve resources files
def _get_resources(package_name):
    # Get all the resources (also on nested levels)
    res_paths = os.path.join(package_name, "resources")
    all_resources = [os.path.join(folder, file) for folder, _, files in os.walk(res_paths) for file in files]
    # Remove the prefix: start just from "resources"
    return [resource[resource.index("resources"):] for resource in all_resources]


# Read requirements
this_location = os.path.dirname(os.path.realpath(__file__))
requirements_file = os.path.join(this_location, "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()

# Read README
readme_file = os.path.join(this_location, "README.md")
with open(readme_file, "r", encoding="utf-8") as f:
    readme = f.read()


# Package configuration
_NAME="piper-tools"
setup(
    name=_NAME,
    version="0.4.0",
    description="A software manager for easy development and distribution of Python code",
    packages=find_packages(),
    package_data={"piper": _get_resources("piper")},
    install_requires=requirements,
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'piper = piper.__main__:main',
        ],
    },

    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/piper-tools/piper",
    author="Federico Pugliese",
    author_email="federico.pugliese.wr@gmail.com",
    license="Apache Software License, Version 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ]
)
