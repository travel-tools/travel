import os


EGG_INFO_SUFFIX = ".egg_info"


def get_egg_info_folders(location: str):
    return [
        d for d in os.listdir(location)
        if os.path.isdir(d) and d.endswith(EGG_INFO_SUFFIX)
    ]
