from pathlib import Path


class ConfigService:
    config_map = {}

    def make_config(self):
        with open(Path('config.txt')) as f:
            for line in f.read().splitlines():
                stem = line.split(",")
                self.config_map[stem[0]] = [tuple(map(int, v.split(":"))) for v in stem[1:]]
        print(self.config_map)
