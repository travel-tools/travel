import re

from piper.config.sanitizers import asserter

_PACKAGE = re.compile(r"^[A-Za-z0-9\-\._]+$")
_VERSION = re.compile(r"^[A-Za-z0-9\-\._]+$")  # To be changed


def sanitize_package(package: str) -> str:
    return asserter.regex(_PACKAGE, package)


def sanitize_version(version: str) -> str:
    return asserter.regex(_VERSION, version)
