import pytest

import db.models
from api import models


@pytest.fixture()
def locations(session):
    locations = [
        db.models.Location(name='testlocation1', description='some desc', score=1),
        db.models.Location(name='testlocation2', description='some desc', score=1),
        db.models.Location(name='testlocation3', description='some desc', score=1),
    ]
    session.bulk_save_objects(locations)


def test_get_all_locations(api_client, locations):
    response = api_client.get('/locations')

    assert response.status_code == 200
    assert len(response.json()) == 3

#
# def test_get_location_by_id(api_client, locations):
#     response = api_client.get('/locations/1')
#
#     assert response.status_code == 200
#     assert response.json()['name'] == 'testlocation1'
