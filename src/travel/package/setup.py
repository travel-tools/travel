from setuptools import setup, find_packages
import os


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
_NAME = "travel"
setup(
    name=_NAME,
    version="0.0.0",
    description="A software manager for easy development and distribution of Python code",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'travel = travel.__main__:main',
        ],
    },

    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/travel-tools/travel",
    author="Federico Pugliese",
    author_email="federico.pugliese.wr@gmail.com",
    license="Apache Software License, Version 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
