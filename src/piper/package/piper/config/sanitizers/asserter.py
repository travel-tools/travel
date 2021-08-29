import re


def regex(matcher: re.Pattern, string: str) -> str:
    assert matcher.match(string)
    return string
