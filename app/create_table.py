from db.base import Base, engine
from model.history import History


Base.metadata.create_all(engine)
