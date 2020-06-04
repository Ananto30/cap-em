import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_uri = os.getenv('DB_URI', 'sqlite:///capem.db')

engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)

Base = declarative_base()
