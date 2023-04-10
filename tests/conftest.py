import base64
import os

import falcon.testing
import pytest


@pytest.fixture(scope="session")
def env_vars():
    os.environ["DB_URI"] = "sqlite+pysqlite:///:memory:"

    config_file_content = ""
    with open("config/example.config.yml", "r", encoding="utf-8") as file:
        config_file_content = file.read()
    os.environ["CONFIG"] = base64.b64encode(config_file_content.encode("utf-8")).decode(
        "utf-8"
    )


@pytest.fixture(scope="session")
def create_tables():
    # import here to avoid start db engine before env_vars fixture
    from src.create_table import create_table  # pylint: disable=import-outside-toplevel

    create_table()


@pytest.fixture
def client(
    env_vars, create_tables
):  # pylint: disable=unused-argument,redefined-outer-name
    # import here to avoid start db engine before env_vars fixture
    from src.app import create_app  # pylint: disable=import-outside-toplevel

    app = create_app()
    return falcon.testing.TestClient(app)
