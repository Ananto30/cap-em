import time

from db.base import Session
from model.history import History
from .config_service import ConfigService


class LimitService:
    _instance = None

    def __init__(self, config_service: ConfigService, db_session: Session):
        LimitService._instance = self
        self.config_service = config_service
        self.db = db_session

    def check_limit(self, config: str, access_id: str) -> (bool, int):
        req_time = time.time()

        for cfg in self.config_service.config_map[config]:
            start_time = req_time - cfg[0]
            c = self.db.query(History) \
                .filter(History.access_id == access_id) \
                .filter(History.access_at >= start_time)

            if c.count() >= cfg[1]:
                item = c.first()
                return False, int(cfg[0] - (req_time - item.access_at))

        return True, 0

    def add_usage(self, config: str, access_id: str):
        req_time = time.time()

        new_record = History(
            access_id=access_id,
            resource_name=config,
            access_at=req_time
        )
        self.db.add(new_record)
        self.db.commit()

    @staticmethod
    def get_instance():
        return ConfigService._instance
