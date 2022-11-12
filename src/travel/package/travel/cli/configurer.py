import logging
import functools
from typing import List

import yaml
from travel.config.environment.configuration import get_config_file_path

logger = logging.getLogger(__name__)


def from_string_to_config(words: List[str], remove: bool) -> dict:

    if not words:
        raise ValueError("Provide at least a value to add/remove after 'travel config add/remove'")
    if not remove and len(words) < 2:
        raise ValueError("Provide at least two values, e.g. travel config add <key> <value>")

    if remove:
        words.append(None)

    return functools.reduce(lambda x, y: {y: x}, reversed(words))


def configure(action: str, config: List[str]):

    path = get_config_file_path()

    # If file exists, read it, else return an empty config and create the file
    if path.exists():
        with open(path) as f:
            current = yaml.load(f, Loader=yaml.SafeLoader) or {}
    else:
        current = {}

    # Get the additional config to add (or remove)
    additional_config = from_string_to_config(config, action == "remove")
    new_config = _merge_dictionaries(current, additional_config)

    # Write it
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(new_config, f, default_flow_style=False)


def _merge_dictionaries(main_dict: dict, new_dict: dict, merging_lists: bool = False) -> dict:
    """Merge two dictionaries prioritizing the second one"""

    # Copy the dict
    main_dict = main_dict.copy()

    # Get all the keys
    main_keys = main_dict.keys()
    new_keys = new_dict.keys()
    keys = set(main_keys).union(new_keys)

    # For each key, merge the dict
    for key in keys:
        # If key is just in new, add it to main
        if key not in main_keys:
            main_dict[key] = new_dict[key]
        # If key is in both dicts, and...
        elif key in new_keys:
            # ...the values are dicts, merge them recursively
            if isinstance(main_dict[key], dict) and isinstance(new_dict[key], dict):
                main_dict[key] = _merge_dictionaries(main_dict[key], new_dict[key], merging_lists=merging_lists)
            # ...the value is NOT a dict in both cases, override the main value
            else:
                # If merging lists is True, and values are lists, concatenate the elements
                if merging_lists and isinstance(main_dict[key], list) and isinstance(new_dict[key], list):
                    main_dict[key] = main_dict[key] + new_dict[key]
                # Override them otherwise
                else:
                    main_dict[key] = new_dict[key]
        # If key is just in main, nothing to do: just keep main_dict as it is

    return main_dict
