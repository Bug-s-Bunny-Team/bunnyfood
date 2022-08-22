from db.utils import gc_distance


def test_get_all_locations(api_client):
    response = api_client.get('/locations/?only_from_followed=false')

    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_all_locations_from_followed(api_client):
    response = api_client.get('/locations/')

    assert response.status_code == 200
    assert len(response.json()) == 2

    locations = response.json()
    assert locations[0]['name'] == 'testlocation4'
    assert locations[1]['name'] == 'testlocation5'


def test_get_location_by_id(api_client):
    response = api_client.get('/locations/1')

    assert response.status_code == 200
    assert response.json()['name'] == 'testlocation1'


def test_get_locations_coords(api_client):
    response = api_client.get('/locations/?only_from_followed=false&lat=55.7255843&long=37.6243329')

    assert response.status_code == 200
    assert response.json()[0]['name'] == 'testlocation4'


def test_get_locations_min_rating(api_client):
    response = api_client.get('/locations/?only_from_followed=false&min_rating=2')

    assert response.status_code == 200

    locations = response.json()
    assert all([l['score'] >= 2 for l in locations])


def test_get_locations_radius(api_client):
    lat = 55.7252037
    long = 37.6284957
    radius = 100

    response = api_client.get(
        f'/locations/?only_from_followed=false&current_lat={lat}&current_long={long}&radius={radius}'
    )

    assert response.status_code == 200

    locations = response.json()
    for l in locations:
        assert gc_distance(lat, long, l['lat'], l['long']) <= 100
