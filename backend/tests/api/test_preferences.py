from db import models


def test_get_user_prefs(api_client):
    result = api_client.get('/preferences/')

    assert result.status_code == 200
    assert result.json()['default_guide_view'] == 'map'


def test_update_user_prefs(api_client, session):
    result = api_client.put('/preferences/', json={
        'default_guide_view': 'list'
    })

    assert result.status_code == 200
    assert result.json()['default_guide_view'] == 'list'

    user = session.query(models.User).filter_by(username='testuser').first()
    assert user.preferences.default_guide_view == 'list'
