from typing import Optional

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db import models
from db.models import Post
from functions.scraping.function.download import Downloader
from functions.scraping.function.scrapers import BaseScraper
from functions.scraping.function.service import ScrapingService

from tests.api.db import populate_db


class DummyScraper(BaseScraper):
    def get_last_post(self, username: str):
        return None

    def get_last_posts(self, username: str, limit: int):
        return []

    def get_post_from_url(self, url: str):
        return None


class DummyDownloader(Downloader):
    def __init__(self):
        super(DummyDownloader, self).__init__('dummy-bucket')

    def download_and_save_post(
        self, post: Post, overwrite: bool = True
    ) -> Optional[str]:
        return 'key'


@pytest.fixture(scope='session')
def engine():
    return create_engine('postgresql://user:password@localhost/bunnyfood_test')


@pytest.fixture
def tables(engine):
    models.Base.metadata.create_all(engine)
    yield
    models.Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    populate_db(session)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def service(session):
    return ScrapingService(scraper=DummyScraper(), downloader=DummyDownloader(), session=session)
