import os
import re

from piper.config.sanitizers import asserter


_BASE_CHARS = r"^[A-Za-z0-9\-\._]+$"
_PACKAGE = re.compile(_BASE_CHARS)
_VERSION = re.compile(_BASE_CHARS)  # To be changed or not?

_MODIFIERS = r"(==|<|<=|>|>=|!=|===|~=)"
_VERSIONED_PACKAGE = r"^"+_BASE_CHARS+r"("+_MODIFIERS+_BASE_CHARS+",)*("+_MODIFIERS+_BASE_CHARS+")? *$"


def sanitize_package(package: str) -> str:
    return asserter.regex(_PACKAGE, package)


def is_just_package(package: str) -> bool:
    return bool(_PACKAGE.match(package))


def sanitize_version(version: str, accept_path=False) -> str:
    if accept_path and os.path.isdir(version):
        return version
    else:
        return asserter.regex(_VERSION, version)


def sanitize_versioned_package(spec: str) -> str:
    return asserter.regex(_VERSIONED_PACKAGE, spec)
