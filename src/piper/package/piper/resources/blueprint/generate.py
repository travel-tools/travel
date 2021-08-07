import argparse
import importlib
import inspect

import yaml
from piperblue.blueprint import PiperBlueprint


def _find(yml, pipe):
    try:
        for p, properties in yml.items():
            if p == pipe:
                return properties
            found = _find(yml[p], pipe)
            if found:
                return found
    except:
        return None


def _generate(file: str, blueprint_name: str, pipe: str, context: str):

    # Find the config
    with open(file) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    properties = _find(yml, pipe)
    config = properties.get("config")

    # Import the blueprint class
    module = f"{blueprint_name}.blueprint"
    blueprint = inspect.getmembers(
        importlib.import_module(module),
        lambda member: inspect.isclass(member) and member.__module__ == module and issubclass(member, PiperBlueprint)
    )[0]

    # Instantiate it and run it
    blueprint[1]().generate(context, config)


def main():

    # Parse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--context")
    parser.add_argument("--pipe")
    parser.add_argument("--blueprint")
    args = parser.parse_args()

    # Generate
    _generate(args.file, args.blueprint, args.pipe, args.context)


if __name__ == '__main__':

    main()
