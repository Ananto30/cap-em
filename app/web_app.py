import logging

from flask import Flask
from flask_restful import Api

from app.api.controller import Controller
from app.db.base import Session
from app.service.config_service import ConfigService
from app.service.limit_service import LimitService

app = Flask("cap-em")
api = Api(app)

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s | %(process)d | %(module)s : %(message)s', level=logging.INFO)

# Initialize services and dependency injections
session = Session()
config_service = ConfigService()
limit_service = LimitService(config_service, session)
config_service.load_config()
controller = Controller(limit_service, config_service, api)
controller.register_routes()
