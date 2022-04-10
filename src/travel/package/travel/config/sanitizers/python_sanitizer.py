import re
from typing import Optional

from travel.config.sanitizers import asserter

_VERSION = re.compile(r"^\d+\.\d+.\d+$")


def sanitize_version(version: str, nullable: bool = False) -> Optional[str]:
    if version is None and nullable:
        return None
    return asserter.regex(_VERSION, version)
