from db import models


def test_get_all_profiles(api_client):
    results = api_client.get('/profiles/')

    assert results.status_code == 200
    assert len(results.json()) == 3


def test_get_followed_profiles(api_client):
    results = api_client.get('/followed/')

    assert results.status_code == 200
    assert len(results.json()) == 2


def test_follow_profile(api_client, session):
    results = api_client.post('/followed/', json={
        'id': 1,
        'username': 'testprofile2'
    })

    assert results.status_code == 201

    followed = session.query(models.SocialProfile).filter_by(id=1).first()
    assert followed.followers[0].username == 'testuser'
