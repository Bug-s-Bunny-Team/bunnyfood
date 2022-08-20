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
    client = TestClient(app)
    client.headers = {
        'Authorization': 'Bearer eyJraWQiOiJVNTBPWjZydmpCZksyY2ZRZGh3UGdkN2t4Z1wvc1dNcU1BUWJXekppWUw3RT0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiaEVHVUNnUlFpX0hkSVljWWw1NHpGUSIsInN1YiI6Ijk0Njc4NjkzLTExMWUtNGQxOS05MzdkLWVlYTIzNThhY2YzYiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV92emx0SHYybVoiLCJjb2duaXRvOnVzZXJuYW1lIjoidGVzdHVzZXIiLCJhdWQiOiIyazVkNGc1ODA3MmV2YmRxbG9xa3Vrc2Q1dSIsImV2ZW50X2lkIjoiOWI4Yzc2YzgtZTZlMS00NWIyLThkMjktYTcwYjgzMWVjNDgyIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NjEwMDQyNzksImV4cCI6MTY2MTA5MDY3OSwiaWF0IjoxNjYxMDA0Mjc5LCJqdGkiOiIxZTkzMGI5Mi04MGQ4LTQwMTMtOWYwYi01Y2ZiMDdmOWYwMTIiLCJlbWFpbCI6InRlc3RAdGVzdC5jb20ifQ.j6PhJb81R-KHguDCswDBISZwPa_i0AZACcr_7kLsluUlCsMOgtj_Hp2PFXwPIcvyTmU_RRqynuGKCc_7COt0Ed6rrINnV1A98vnRI_EjPAKAMFZbhr003P75Mq77qSO7e_d_rG17gci-jinvGEH4nRhO0n9rKRX4y5wPv2VP9Bhlcd5blYnB0GTnzdiUFaQfNKUaIY7cryJkC2HX4i_ULObL7CU3Xmt7gcDUYiO6H5ort1RHMsECTNbtNBUkb4zvVoCDrH7nLmYip5t4YuLO9SatUw9kbMkpJhXRrxrmKN0KaWkX0aYk-LO64tRVWp5Bh7Ttutctc-9Up4X6VtXw1w'
    }
    yield client
    app.dependency_overrides.clear()
