
class ConfigService:
    config_map = {}

    def make_config(self):
        # TODO: read config from file
        self.config_map['email'] = [(60, 1), (3600, 2), (86400, 5)]
