from datetime import datetime

from sqlalchemy.orm import Session

from src.model.history import History
from src.stores.file_store import ConfigFileStore


class UsageStore:
    """
    Keeps track of the resource usage.
    """

    def __init__(self, db_session: Session, config_store: ConfigFileStore):
        self._db = db_session
        self._config_store = config_store

    def add_usage(self, resource_name: str, access_id: str) -> None:
        """
        Add a new usage record.
        """
        req_time = now()

        new_record = History(
            access_id=access_id,
            resource_name=resource_name,
            access_at=req_time,
        )
        self._db.add(new_record)
        self._db.commit()

    def get_usage(self, resource_name: str, access_id: str) -> int:
        """
        Get the usage of the resource.
        Returns the number of milliseconds until the next request can be made.
        """
        req_time = now()

        for cfg in self._config_store.config_map[resource_name]:
            interval = cfg[0] * 1000  # Convert to milliseconds
            limit = cfg[1]

            start_time = req_time - interval
            histories = (
                self._db.query(History)
                .filter(History.resource_name == resource_name)
                .filter(History.access_id == access_id)
                .filter(History.access_at >= start_time)
                # .order_by(History.access_at.desc())
            )

            if histories.count() >= limit:
                item = histories.first()
                if item is not None:
                    return interval - (req_time - item.access_at)

        return 0


def now() -> int:
    """
    Get the current time in milliseconds.
    """
    return int(datetime.utcnow().timestamp() * 1000)
