import pytest

from api.s4 import s4
from db import models


def test_get_all_unfollowed_profiles(api_client):
    results = api_client.get('/profiles/')

    assert results.status_code == 200

    results = results.json()
    assert len(results) == 3
    assert results[0]['username'] == 'testprofile2'
    assert results[1]['username'] == 'testprofile4'
    assert results[2]['username'] == 'testprofile5'


def test_get_all_profiles(api_client):
    results = api_client.get('/profiles/?unfollowed_only=false')

    assert results.status_code == 200

    results = results.json()
    assert len(results) == 5


def test_get_followed_profiles(api_client):
    results = api_client.get('/followed/')

    assert results.status_code == 200
    results = results.json()
    assert len(results) == 2
    assert results[0]['username'] == 'testprofile1'
    assert results[1]['username'] == 'testprofile3'


@pytest.mark.vcr
def test_follow_profile(api_client, session):
    results = api_client.post('/followed/', json={'username': 'antoniorazzi'})

    assert results.status_code == 201

    followed = session.query(models.SocialProfile).filter_by(id=1).first()
    assert followed.followers[0].username == 'testuser'


@pytest.mark.vcr
def test_follow_unexisting_user(api_client, session):
    results = api_client.post('/followed/', json={'username': 'thissurelydoesnotexist43058'})

    assert results.status_code == 404


def test_unfollow_profile(api_client, session):
    results = api_client.post('/followed/unfollow/', json={'username': 'testprofile3'})

    assert results.status_code == 200

    unfollowed = session.query(models.SocialProfile).filter_by(id=3).first()
    assert len(unfollowed.followers) == 0


def test_get_popular_profiles(api_client):
    results = api_client.get('/profiles/popular/5')

    assert results.status_code == 200

    results = results.json()
    assert len(results) == 3
    assert results[0]['username'] == 'testprofile4'
    assert results[1]['username'] == 'testprofile5'
    assert results[2]['username'] == 'testprofile2'


@pytest.mark.vcr
def test_profiles_search_existing(api_client):
    results = api_client.get('/profiles/search/testprofile4')

    assert results.status_code == 200
    assert results.json()['username'] == 'testprofile4'
    assert len(s4.runs) == 0


@pytest.mark.vcr
def test_profiles_search_following(api_client):
    results = api_client.get('/profiles/search/testprofile1')

    assert results.status_code == 204
    assert not results.json()
    assert len(s4.runs) == 0


@pytest.mark.vcr
def test_profiles_search_not_existing(api_client):
    results = api_client.get('/profiles/search/thissurelydoesnotexist43058')

    assert results.status_code == 404
    assert len(s4.runs) == 0


@pytest.mark.vcr
def test_profiles_search_existing_and_create(api_client):
    results = api_client.get('/profiles/search/antoniorazzi')

    assert results.status_code == 201
    assert results.json()['username'] == 'antoniorazzi'
    assert len(s4.runs) == 1
