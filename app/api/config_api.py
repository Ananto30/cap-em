from flask_restful import Resource

from app.service.config_service import ConfigService


class Config(Resource):

    def __init__(self, **kwargs):
        self.config_service: ConfigService = kwargs['config_service']

    # TODO: IMPORTANT!! For now the cache is in memory, so we can't update cache in all workers,
    #  may be a candidate of redis/memcached
    # def post(self):
    #     self.config_service.make_config()
    #     return

    def get(self):
        data = self.config_service.config_map
        return data
