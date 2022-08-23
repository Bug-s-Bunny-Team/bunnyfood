import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker()
Base = declarative_base()


def create_connection_url(user: str, password: str, host: str, db: str):
    return f'postgresql://{user}:{password}@{host}/{db}'


def configure_session(
    user=os.environ.get('DB_USER', 'user'),
    password=os.environ.get('DB_PASS', 'password'),
    host=os.environ.get('DB_HOST', 'localhost'),
    db=os.environ.get('DB_NAME', 'bunnyfood_dev'),
    engine: Optional[Engine] = None,
):
    if not engine:
        engine = create_engine(create_connection_url(user, password, host, db))
    SessionLocal.configure(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal
