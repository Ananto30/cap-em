import time
from db.base import Session
from model.history import History
from .config_service import ConfigService


class LimitService:

    def __init__(self, config_service: ConfigService, db_session: Session):
        self.config_service = config_service
        self.db = db_session

    def check_limit(self, config, access_id):
        req_time = time.time()

        for cfg in self.config_service.config_map[config]:
            start_time = req_time - cfg[0]
            c = self.db.query(History)\
                .filter(History.access_id == access_id)\
                .filter(History.access_at >= start_time)\
                .count()
            print(c)
            if c >= cfg[1]:
                return False

        return True

    def add_usage(self, config, access_id):
        req_time = time.time()

        new_record = History(
            access_id=access_id,
            resource_name=config,
            access_at=req_time
        )
        self.db.add(new_record)
        self.db.commit()
