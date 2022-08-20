import pytest

from db import models


@pytest.fixture()
def profiles(session):
    profiles = [
        models.SocialProfile(username='testprofile1'),
        models.SocialProfile(username='testprofile2'),
        models.SocialProfile(username='testprofile3'),
    ]
    session.bulk_save_objects(profiles)


def test_get_all_profiles(api_client, profiles):
    results = api_client.get('/profiles')

    assert results.status_code == 200
    assert len(results.json()) == 3
