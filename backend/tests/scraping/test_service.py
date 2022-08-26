from dataclasses import dataclass
from typing import List

from instaloader import Post as InstaPost

from functions.scraping.function.models import ScrapingEvent


@dataclass
class DummyLocation:
    id: int
    name: str
    slug: str
    has_public_page: bool
    lat: float
    lng: float


def _add_location(posts: List[InstaPost]):
    l = {
        "id": 244300930,
        "name": "Senato della Repubblica",
        "slug": "senato-della-repubblica",
        "has_public_page": True,
        "lat": 41.8991509092,
        "lng": 12.4748724092,
    }
    for p in posts:
        p._location = DummyLocation(**l)


def test_service_no_posts(service):
    service._scraper._posts = []

    response = service.process_event(ScrapingEvent(username='antoniorazzi'))

    assert response['posts_count'] == 0


def test_service_n_posts(service):
    _add_location(service._scraper._posts[-3:])

    response = service.process_event(ScrapingEvent(username='antoniorazzi'))

    assert response['posts_count'] == 3
    assert len(response['posts']) == 3


def test_service_limit_posts(service):
    _add_location(service._scraper._posts)

    response = service.process_event(
        ScrapingEvent(username='antoniorazzi', posts_limit=2)
    )

    assert response['posts_count'] == 2
    assert len(response['posts']) == 2
