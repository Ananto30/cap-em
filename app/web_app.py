from flask import Flask
from flask_restful import Api

from api.controller import Controller
from db.base import Session
from service.config_service import ConfigService
from service.limit_service import LimitService

app = Flask(__name__)
api = Api(app)

# Initialize services and dependency injections
session = Session()
config_service = ConfigService()
limit_service = LimitService(config_service, session)
config_service.make_config()
controller = Controller(limit_service, config_service, api)
controller.register_routes()
