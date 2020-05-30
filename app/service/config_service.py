import logging
from pathlib import Path


class ConfigService:
    _instance = None
    config_map = {}

    def __init__(self, config_location='config/config.txt'):
        ConfigService._instance = self
        self.config_location = config_location

    def load_config(self):
        with open(Path(self.config_location)) as f:
            for line in f.read().splitlines():
                stem = line.split(",")
                self.config_map[stem[0]] = [tuple(map(int, v.split(":"))) for v in stem[1:]]
        logging.info(self.config_map)

    @staticmethod
    def get_instance():
        return ConfigService._instance
