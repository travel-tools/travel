import os
from typing import Dict, Any

from piperblue.blueprint import PiperBlueprint


class PiperBlueprintExample(PiperBlueprint):

    def get_file_and_folders_renamings(self, context: str, config: Dict[str, Any]) -> Dict[str, str]:

        # Parse the config
        package_name = config["package"]["name"]
        package_folder = os.path.join(context, "package")
        return {
            os.path.join(package_folder, "packagename"): os.path.join(package_folder, package_name)
        }

    def get_substitutions_in_files(self, config: Dict[str, Any]) -> Dict[str, str]:

        # Parse the config
        python = config["python"]
        package = config["package"]
        package_name = package["name"]
        description = package["description"]
        return {
            "package_name": package_name,
            "description": description,
            "python_version": python
        }
