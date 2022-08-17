def test_get_all_locations(api_client):
    locations = api_client.get('/locations')

    assert locations.status_code == 200
    assert len(locations.json()) > 0


def test_get_location_by_id(api_client):
    location = api_client.get('/locations/666')

    assert location.status_code == 200
    assert location.json()['id'] == 666
