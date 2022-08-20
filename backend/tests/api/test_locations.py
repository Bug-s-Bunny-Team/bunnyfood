from sqlalchemy.orm import Session

from api import models


def test_get_all_locations(api_client, session: Session):
    locations = [
        models.Location(name='testlocation1', description='some desc', score=1),
        models.Location(name='testlocation2', description='some desc', score=1),
        models.Location(name='testlocation3', description='some desc', score=1)
    ]

    session.bulk_save_objects(locations)
    response = api_client.get('/locations')
    session.rollback()

    assert response.status_code == 200
    assert len(response.json()) == 3
