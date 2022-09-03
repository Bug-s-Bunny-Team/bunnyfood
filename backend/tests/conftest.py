import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import populate_db
from db import create_connection_url, models


@pytest.fixture(scope='session')
def vcr_config():
    return {'record_mode': 'once'}


@pytest.fixture(scope='session')
def engine():
    return create_engine(
        create_connection_url('user', 'password', 'localhost', 'bunnyfood_test')
    )


@pytest.fixture
def tables(engine):
    models.Base.metadata.create_all(engine)
    yield
    models.Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    populate_db(session)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
