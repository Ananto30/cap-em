from flask import Flask
from flask_restful import Api
from service.limit_service import LimitService
from service.config_service import ConfigService
from db.base import Session

from api.controller import Controller

app = Flask(__name__)
api = Api(app)

session = Session()
config_service = ConfigService()
limit_service = LimitService(config_service, session)
config_service.make_config()
controller = Controller(limit_service, config_service, api)

if __name__ == '__main__':
    app.run(debug=True)
