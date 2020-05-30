from api.config_api import Config
from api.limit_api import CheckLimit, AddUsage


class Controller:

    def __init__(self, limit_service, config_service, api):
        self.limit_service = limit_service
        self.config_service = config_service
        self.api = api

    def register_routes(self):
        self.api.add_resource(CheckLimit, '/limit/check', resource_class_kwargs={'limit_service': self.limit_service})
        self.api.add_resource(AddUsage, '/add/usage', resource_class_kwargs={'limit_service': self.limit_service})
        self.api.add_resource(Config, '/config', resource_class_kwargs={'config_service': self.config_service})
