import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.dependencies import get_db
from api.main import app
from db import models
from db.models import Base


def populate_db(session):
    profiles = [
        models.SocialProfile(id=1, username='testprofile1'),
        models.SocialProfile(id=2, username='testprofile2'),
        models.SocialProfile(id=3, username='testprofile3'),
    ]
    session.add_all(profiles)

    users = [
        models.User(id=2, username='testuser1'),
        models.User(id=3, username='testuser2'),
        models.User(id=4, username='testuser3'),
    ]
    session.add_all(users)

    locations = [
        models.Location(id=1, name='testlocation1', description='some desc', score=1),
        models.Location(id=2, name='testlocation2', description='some desc', score=1),
        models.Location(id=3, name='testlocation3', description='some desc', score=1),
        models.Location(id=4, name='testlocation4', description='some desc', score=4),
        models.Location(id=5, name='testlocation5', description='some desc', score=4),
        models.Location(
            id=6,
            name='testlocation6',
            description='some desc',
            score=4,
            lat=43.5,
            long=53.4,
        ),
    ]
    session.add_all(locations)

    user = models.User(id=1, username='testuser')
    user.followed_profiles.append(profiles[0])
    user.followed_profiles.append(profiles[2])
    session.add(user)

    session.commit()


@pytest.fixture(scope='session')
def engine():
    return create_engine('postgresql://user:password@localhost/bunnyfood_test')


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


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


@pytest.fixture
def api_client(session: Session):
    def get_db_override():
        return session

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    client.headers = {
        'Authorization': 'Bearer eyJraWQiOiJVNTBPWjZydmpCZksyY2ZRZGh3UGdkN2t4Z1wvc1dNcU1BUWJXekppWUw3RT0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiaEVHVUNnUlFpX0hkSVljWWw1NHpGUSIsInN1YiI6Ijk0Njc4NjkzLTExMWUtNGQxOS05MzdkLWVlYTIzNThhY2YzYiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV92emx0SHYybVoiLCJjb2duaXRvOnVzZXJuYW1lIjoidGVzdHVzZXIiLCJhdWQiOiIyazVkNGc1ODA3MmV2YmRxbG9xa3Vrc2Q1dSIsImV2ZW50X2lkIjoiOWI4Yzc2YzgtZTZlMS00NWIyLThkMjktYTcwYjgzMWVjNDgyIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NjEwMDQyNzksImV4cCI6MTY2MTA5MDY3OSwiaWF0IjoxNjYxMDA0Mjc5LCJqdGkiOiIxZTkzMGI5Mi04MGQ4LTQwMTMtOWYwYi01Y2ZiMDdmOWYwMTIiLCJlbWFpbCI6InRlc3RAdGVzdC5jb20ifQ.j6PhJb81R-KHguDCswDBISZwPa_i0AZACcr_7kLsluUlCsMOgtj_Hp2PFXwPIcvyTmU_RRqynuGKCc_7COt0Ed6rrINnV1A98vnRI_EjPAKAMFZbhr003P75Mq77qSO7e_d_rG17gci-jinvGEH4nRhO0n9rKRX4y5wPv2VP9Bhlcd5blYnB0GTnzdiUFaQfNKUaIY7cryJkC2HX4i_ULObL7CU3Xmt7gcDUYiO6H5ort1RHMsECTNbtNBUkb4zvVoCDrH7nLmYip5t4YuLO9SatUw9kbMkpJhXRrxrmKN0KaWkX0aYk-LO64tRVWp5Bh7Ttutctc-9Up4X6VtXw1w'
    }
    yield client
    app.dependency_overrides.clear()
