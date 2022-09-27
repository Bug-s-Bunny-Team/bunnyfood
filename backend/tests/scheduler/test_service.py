import pytest
from datetime import datetime, timedelta

from tests.mocks import SFNMock

from db import models
from functions.scheduler.function.service import SchedulerService, SchedulerEvent


@pytest.fixture
def service(session):
    return SchedulerService(session, 'dummy-arn')


@pytest.fixture
def profiles(session):
    now = datetime.now()

    profiles = [
        models.SocialProfile(
            username='should_be_scraped_now_1',
            last_scraped=now - timedelta(hours=1, minutes=30),
        ),
        models.SocialProfile(
            username='should_be_scraped_now_2', last_scraped=now - timedelta(hours=2)
        ),
        models.SocialProfile(
            username='should_not_be_scraped_now',
            last_scraped=now - timedelta(minutes=30),
        ),
    ]

    session.add_all(profiles)
    session.commit()


def test_get_profiles(service, profiles):
    profiles = service._get_profiles(last_scrape_gte=1)

    assert len(profiles) == 2
    assert profiles[0].username == 'should_be_scraped_now_2'
    assert profiles[1].username == 'should_be_scraped_now_1'


def test_process_event(service, profiles):
    service._client = SFNMock()

    event = SchedulerEvent()
    service.process_event(event)

    assert service._client.started
