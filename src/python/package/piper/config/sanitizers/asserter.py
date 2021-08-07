import re


def regex(matcher: re.Pattern, string: str) -> str:
    matcher.match(string)
    return string
