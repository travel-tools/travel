import re

from piper.config.sanitizers import asserter

_NAME = re.compile(r"^[A-Za-z0-9\-\._]+$")


def sanitize_name(name: str) -> str:
    return asserter.regex(_NAME, name)
