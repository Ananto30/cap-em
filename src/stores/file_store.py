import os
from typing import Dict, List, Tuple

import yaml


class FileStore:
    """
    A simple file store that can be used to store and retrieve data from a file.
    """

    def __init__(self, path):
        self.path = path

    def get(self) -> str:
        """
        Get the contents of the file.
        """
        with open(self.path, "r", encoding="utf-8") as file:
            return file.read()

    def set(self, value: str) -> None:
        """
        Set the contents of the file.
        """
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(value)


class ConfigFileStore(FileStore):
    """
    A file store that can be used to store and retrieve configuration data in YAML format.
    """

    config_map: Dict[str, List[Tuple[int, int]]] = {}

    def get_configs(self) -> str:
        """
        Get the contents of the file as yaml.
        """
        return yaml.safe_load(self.get())

    def update_configs(
        self,
        raw_content: str,
        config_map: Dict[str, List[Tuple[int, int]]],
    ) -> None:
        """
        Set the contents of the file from a dictionary.
        """
        self.set(yaml.safe_dump(raw_content))
        self.config_map = config_map
