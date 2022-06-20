import os


EGG_INFO_SUFFIX = ".egg-info"


def get_egg_info_folders(location: str):
    return [
        d for d in os.listdir(location)
        if d.endswith(EGG_INFO_SUFFIX)
    ]
