from sqlalchemy import Column, String, Integer
from db.base import Base


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    access_id = Column(String, index=True)
    resource_name = Column(String)
    access_at = Column(Integer)
