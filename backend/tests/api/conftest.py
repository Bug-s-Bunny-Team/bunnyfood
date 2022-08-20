import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.dependencies import get_db
from api.main import app
from db.models import Base


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine('postgresql://user:password@localhost/bunnyfood_test')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with SessionLocal() as db:
        Base.metadata.create_all(engine)
        yield db
        db.rollback()


@pytest.fixture(name='api_client')
def api_fixture(session: Session):
    def get_db_override():
        return session

    app.dependency_overrides[get_db] = get_db_override
    yield TestClient(app)
    app.dependency_overrides.clear()
