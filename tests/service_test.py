import os
import time

from app.create_table import create_table
from app.db.base import Session
from app.service.config_service import ConfigService
from app.service.limit_service import LimitService

# TODO: Maybe a candidate for class based approach
#  in that case need to fix the `db/base.py`
ut_db = "capem-ut.db"

# Initialize services
session = Session()
config_service = ConfigService(config_location="tests/config.txt")
limit_service = LimitService(config_service, session)


def test_instance():
    assert config_service == config_service.get_instance()
    assert limit_service == limit_service.get_instance()


def test_load_config():
    assert config_service.config_map == {}
    config_service.load_config()
    assert config_service.config_map == {
        "download": [(60, 3), (3600, 5), (86400, 8)],
        "email": [(5, 2), (20, 4), (40, 6)],
    }


def test_email_limit():
    create_table()

    assert limit_service.check_limit("email", "ananto") == (True, 0)
    limit_service.add_usage("email", "ananto")
    assert limit_service.check_limit("email", "ananto") == (True, 0)
    limit_service.add_usage("email", "ananto")
    # 2 times used, so this time will be a 5 sec cooldown
    assert limit_service.check_limit("email", "ananto") == (False, 5)
    time.sleep(5)

    assert limit_service.check_limit("email", "ananto") == (True, 0)
    limit_service.add_usage("email", "ananto")
    assert limit_service.check_limit("email", "ananto") == (True, 0)
    limit_service.add_usage("email", "ananto")
    # 2 times used, so this time will be a 5 sec cooldown
    assert limit_service.check_limit("email", "ananto") == (False, 5)
    time.sleep(5)

    # 4 times used so there should be a 20 sec cooldown, but we have passed 10 sec already
    assert limit_service.check_limit("email", "ananto") == (False, 10)
    time.sleep(10)

    assert limit_service.check_limit("email", "ananto") == (True, 0)
    limit_service.add_usage("email", "ananto")
    assert limit_service.check_limit("email", "ananto") == (True, 0)
    limit_service.add_usage("email", "ananto")
    # 2 times used, so this time will be a 5 sec cooldown
    assert limit_service.check_limit("email", "ananto") == (False, 5)
    time.sleep(5)

    # 6 times used so there should be a 40 sec cooldown, but we have passed 25 sec already
    assert limit_service.check_limit("email", "ananto") == (False, 15)


# Remove the sqlite db for next ut
os.remove(ut_db) if os.path.isfile(ut_db) else None
