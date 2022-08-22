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
    results = api_client.post('/followed/', json={'username': 'antoniorazzi'})

    assert results.status_code == 201

    followed = session.query(models.SocialProfile).filter_by(id=1).first()
    assert followed.followers[0].username == 'testuser'


def test_unfollow_profile(api_client, session):
    results = api_client.post('/followed/unfollow/', json={'username': 'testprofile3'})

    assert results.status_code == 200

    unfollowed = session.query(models.SocialProfile).filter_by(id=3).first()
    assert len(unfollowed.followers) == 0


def test_get_popular_profiles(api_client):
    results = api_client.get('/profiles/popular/10')

    assert results.status_code == 200


def test_profiles_search_existing(api_client):
    results = api_client.get('/profiles/search/testprofile1')

    assert results.status_code == 200
    assert results.json()['username'] == 'testprofile1'


def test_profiles_search_not_existing(api_client):
    results = api_client.get('/profiles/search/thissurelydoesnotexist43058')

    assert results.status_code == 404


def test_profiles_search_existing_and_create(api_client):
    results = api_client.get('/profiles/search/antoniorazzi')

    assert results.status_code == 201
    assert results.json()['username'] == 'antoniorazzi'
