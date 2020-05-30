import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = os.getenv('DB_URL', 'postgres://capem:pass@localhost:5432/postgres')

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()
