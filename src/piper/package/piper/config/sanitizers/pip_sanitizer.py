import os
import re

from piper.config.sanitizers import asserter

_PACKAGE = re.compile(r"^[A-Za-z0-9\-\._]+$")
_VERSION = re.compile(r"^[A-Za-z0-9\-\._]+$")  # To be changed


def sanitize_package(package: str) -> str:
    return asserter.regex(_PACKAGE, package)


def sanitize_version(version: str, accept_path=False) -> str:
    if accept_path and os.path.isdir(version):
        return version
    else:
        return asserter.regex(_VERSION, version)


def sanitize_package_with_version(spec: str) -> str:
    name, version = spec.split("==")
    sanitize_package(name)
    sanitize_version(version)
    return spec