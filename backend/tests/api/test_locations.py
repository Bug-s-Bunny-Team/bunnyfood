def test_get_all_locations(api_client):
    response = api_client.get('/locations/')

    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_location_by_id(api_client):
    response = api_client.get('/locations/1')

    assert response.status_code == 200
    assert response.json()['name'] == 'testlocation1'


def test_get_locations_coords(api_client):
    response = api_client.get('/locations/?lat=43.5&long=53.4')

    assert response.status_code == 200
    assert response.json()[0]['id'] == 6


def test_get_locations_min_rating(api_client):
    response = api_client.get('/locations/?min_rating=2')

    assert response.status_code == 200

    locations = response.json()
    assert all([l['score'] >= 2 for l in locations])
