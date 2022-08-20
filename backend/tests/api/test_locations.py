def test_get_all_locations(api_client):
    response = api_client.get('/locations/')

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_location_by_id(api_client):
    response = api_client.get('/locations/1')

    assert response.status_code == 200
    assert response.json()['name'] == 'testlocation1'
