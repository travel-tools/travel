import argparse
import re


def replace(file: str, regex: str, replacement: str):

    with open(file) as f:
        content = f.read()
    content = re.sub(regex, replacement, content)
    with open(file, "w") as f:
        f.write(content)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("regex")
    parser.add_argument("replacement")
    args = parser.parse_args()

    replace(args.file, args.regex, args.replacement)
