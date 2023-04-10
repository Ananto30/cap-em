import logging

import falcon.asgi
from falcon.errors import HTTPRouteNotFound  # pylint: disable=no-name-in-module

from src.api.defaults import handle_404
from src.api.rest import Configs, Help, Usage
from src.config_loader import load_config_from_env
from src.db.base import Session
from src.stores.file_store import ConfigFileStore
from src.stores.usage_store import UsageStore

logging.basicConfig(
    format="%(asctime)s | %(process)d | %(module)s : %(message)s",
    level=logging.INFO,
)

CONFIG_PATH = "./internal/configs.yml"


# Initialize the REST API
def create_app():
    """
    Create the REST API.
    """

    # Initialize services and dependency injections
    config_store = ConfigFileStore(CONFIG_PATH)
    session = Session()
    usage_store = UsageStore(session, config_store)

    load_config_from_env(config_store)

    app = falcon.asgi.App()

    app.add_route("/api/v1/help", Help())
    app.add_route("/api/v1/usage/{resource_name}", Usage(usage_store))
    app.add_route("/api/v1/configs", Configs(config_store))

    app.add_error_handler(HTTPRouteNotFound, handle_404)

    return app
