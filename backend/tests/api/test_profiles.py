def test_get_all_profiles(api_client):
    results = api_client.get('/profiles')

    assert results.status_code == 200
    assert len(results.json()) == 3
