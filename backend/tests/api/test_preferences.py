def test_get_user_prefs(api_client):
    result = api_client.get('/preferences/')

    assert result.status_code == 200
    assert result.json()['default_guide_view'] == 'map'