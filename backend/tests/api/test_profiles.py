import pytest

import db.models
from api import models


@pytest.fixture()
def profiles(session):
    profiles = [
        db.models.SocialProfile(username='testprofile1'),
        db.models.SocialProfile(username='testprofile2'),
        db.models.SocialProfile(username='testprofile3'),
    ]
    session.bulk_save_objects(profiles)


def test_get_all_profiles(api_client, profiles):
    results = api_client.get('/profiles')

    assert results.status_code == 200
    assert len(results.json()) == 3
