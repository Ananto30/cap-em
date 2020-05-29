from db.base import Base, engine
from model.history import History

History
Base.metadata.create_all(engine)
