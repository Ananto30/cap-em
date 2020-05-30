from app.db.base import Base, engine
from app.model.history import History


def create_table():
    History
    Base.metadata.create_all(engine)


create_table()
