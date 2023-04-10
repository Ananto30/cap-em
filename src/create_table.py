from src.db.base import Base, engine
from src.model.history import History


def create_table():
    History  # pylint: disable=pointless-statement
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_table()
