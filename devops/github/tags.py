import argparse

import requests


def get_last(repository: str) -> str:
    tags = requests.get(url=f"https://api.github.com/repos/{repository}/git/refs/tags").json()
    return max([t["ref"] for t in tags])


def get_next(tag: str, major: bool, hotfix: bool) -> str:
    maj, minor, patch = tuple(int(x) for x in tag.split("/")[-1].split("."))
    maj = maj + 1 if major else maj
    minor = minor + 1 if not major and not hotfix else (0 if major else minor)
    patch = patch + 1 if not major and hotfix else 0
    return f"{maj}.{minor}.{patch}"


def main(repository: str, major: bool, hotfix: bool):

    tag = get_last(repository)
    next = get_next(tag, major, hotfix)
    print(next)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("repository")
    parser.add_argument("release_branch")
    parser.add_argument("--major", action="store_true")
    parser.add_argument("--hotfix", action="store_true")
    args = parser.parse_args()

    major = args.major or "/major/" in args.release_branch
    hotfix = args.hotfix or "hotfix/" in args.release_branch

    main(args.repository, major, hotfix)
