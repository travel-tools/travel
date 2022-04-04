import os
import re
from typing import Optional

from piper.config.sanitizers import asserter


LATEST_PIP = "latest"

_BASE_CHARS = r"[A-Za-z0-9\-\.\[,\]_]+"  # Support the package[extra1,extra2] syntax
_PACKAGE_NAME = re.compile(_BASE_CHARS)
_PACKAGE = re.compile(r"^"+_BASE_CHARS+r"$")
_VERSION = re.compile(r"^"+_BASE_CHARS+r"$")  # To be changed or not?

_MODIFIERS = r"(==|<|<=|>|>=|!=|===|~=)"
_VERSIONS_M = r"[A-Za-z0-9\-\._\*]+"
_VERSIONED_PACKAGE = re.compile(r"^"+_BASE_CHARS+r"("+_MODIFIERS+_VERSIONS_M+", *)*("+_MODIFIERS+_VERSIONS_M+")? *$")


def sanitize_package(package: str) -> str:
    return asserter.regex(_PACKAGE, package)


def is_just_package(package: str) -> bool:
    return bool(_PACKAGE.match(package))


def sanitize_version(version: str, accept_path=False) -> str:
    if accept_path and os.path.isdir(version):
        return version
    else:
        return asserter.regex(_VERSION, version)


def sanitize_pip_version(version: str, nullable: bool = False) -> Optional[str]:
    if version is None and nullable:
        return None
    else:
        return version == LATEST_PIP or asserter.regex(_VERSION, version)


def sanitize_versioned_package(spec: str) -> str:
    return asserter.regex(_VERSIONED_PACKAGE, spec)


def get_package_name(spec: str, standardize: bool = False) -> str:
    return _PACKAGE_NAME.match(spec).group(0).lower().replace("-", "_")
