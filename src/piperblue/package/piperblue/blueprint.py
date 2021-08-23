import abc
import os
import re
import shutil
from typing import Dict, Any


class PiperBlueprint(abc.ABC):

    def generate(self, resources_folder: str, context: str, config: Dict[str, Any]) -> None:

        # Copy the folder
        pipe = os.path.join(resources_folder, "blueprint")
        copy_tree(pipe, context)

        # Dynamic content generation
        self.dynamic_generate(resources_folder, context, config)
    
        # Make substitutions
        self.substitute(context, config)

    def substitute(self, context: str, config: Dict[str, Any]) -> None:

        # Rename the files and folders
        files_and_folders = self.get_file_and_folders_renamings(context, config)
        for source, dest in files_and_folders.items():
            os.rename(source, dest)

        # Get substitutions to apply
        substitutions = self.get_substitutions_in_files(config)
        replacements = {re.escape("{{"+k+"}}"): v for k, v in substitutions.items()}
        pattern = re.compile("|".join(replacements.keys()))
        # Substitute placeholders
        for root, _, files in os.walk(context):
            for file in files:
                # Read file
                print(os.path.join(root,file))
                with open(os.path.join(root, file), encoding="utf-8") as f:
                    content = f.read()
                # Replace
                replaced = pattern.sub(lambda m: replacements[re.escape(m.group(0))], content)
                # Rewrite file
                with open(os.path.join(root, file), "w", encoding="utf-8") as f:
                    f.write(replaced)

    def dynamic_generate(self, resources_folder: str, context: str, blueprint: Dict[str, Any]) -> None:
        pass

    @abc.abstractmethod
    def get_file_and_folders_renamings(self, context: str, config: Dict[str, Any]) -> Dict[str, str]:
        pass

    @abc.abstractmethod
    def get_substitutions_in_files(self, config: Dict[str, Any]) -> Dict[str, str]:
        pass


def copy_tree(source, destination):
    return shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
