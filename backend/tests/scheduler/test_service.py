import pytest
from datetime import datetime, timedelta

from db import models
from functions.scheduler.function.service import SchedulerService


@pytest.fixture
def service(session):
    return SchedulerService(session, 'dummy-arn')


def test_get_profiles(service):
    session = service._session
    now = datetime.now()

    profiles = [
        models.SocialProfile(
            username='should_be_scraped_now_1',
            last_scraped=now - timedelta(hours=1, minutes=30),
        ),
        models.SocialProfile(
            username='should_be_scraped_now_2', last_scraped=now - timedelta(hours=2)
        ),
        models.SocialProfile(username='should_not_be_scraped_now', last_scraped=now - timedelta(minutes=30)),
    ]
    session.add_all(profiles)
    session.commit()

    profiles = service._get_profiles(last_scrape_gte=1)
    assert len(profiles) == 2
    assert profiles[0].username == 'should_be_scraped_now_2'
    assert profiles[1].username == 'should_be_scraped_now_1'
