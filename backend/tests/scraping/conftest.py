from typing import Optional, List

import pytest

from db.models import Post
from functions.scraping.function.download import Downloader
from functions.scraping.function.models import ScrapedPost, LocationData
from functions.scraping.function.scrapers import BaseScraper
from functions.scraping.function.service import ScrapingService


def _get_post(shortcode: str, location_data: LocationData):
    return ScrapedPost(
        shortcode,
        'https://someurl.com/image.jpg',
        'some caption',
        'some desc',
        'Fancy Restaurant',
        location_data,
    )


class DummyScraper(BaseScraper):
    def get_last_post(self, username: str) -> Optional[ScrapedPost]:
        return _get_post('sdjkfhsfd', LocationData(lat=54.3, long=45.3))

    def get_last_posts(self, username: str, limit: int) -> List[ScrapedPost]:
        return [
            _get_post(f'jdnf{i}', LocationData(lat=54.3, long=45.3))
            for i in range(limit)
        ]


class DummyDownloader(Downloader):
    def __init__(self):
        super(DummyDownloader, self).__init__('dummy-bucket')

    def download_and_save_post(
        self, post: Post, overwrite: bool = True
    ) -> Optional[str]:
        return post.shortcode


@pytest.fixture
def service(session):
    return ScrapingService(
        scraper=DummyScraper(), downloader=DummyDownloader(), session=session
    )
