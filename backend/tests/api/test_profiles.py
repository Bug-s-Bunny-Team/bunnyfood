def test_get_all_profiles(api_client):
    locations = api_client.get('/profiles')

    assert locations.status_code == 200
    assert len(locations.json()) > 0


def test_get_profile_by_id(api_client):
    profile = api_client.get('/profiles/666')

    assert profile.status_code == 200
    assert profile.json()['id'] == 666
