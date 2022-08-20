import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://{user}:{password}@{host}/{db}'.format(
    user=os.environ.get('DB_USER', 'user'),
    password=os.environ.get('DB_PASS', 'password'),
    host=os.environ.get('DB_HOST', 'localhost'),
    db=os.environ.get('DB_NAME', 'bunnyfood_dev'),
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()