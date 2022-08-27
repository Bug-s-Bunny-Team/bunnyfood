import typing
from dataclasses import dataclass
from typing import Optional

from bs4 import Tag

from common.models import LambdaEvent

if typing.TYPE_CHECKING:
    from .scrapers import GramhirScraper


class ScrapingEvent(LambdaEvent):
    username: str
    posts_limit: int = 6


@dataclass
class GramhirPost:
    image_url: str
    details_url: str
    caption: str
    shortcode: str
    location_name: Optional[str]
    location_data: Optional[dict] = None

    @classmethod
    def from_soup_result(cls, result: Tag, scraper: 'GramhirScraper'):
        location = result.find(attrs={'class': 'photo-location'}).get_text(strip=True)
        location = location if location else None

        details_url = result.find('a').get('href')
        shortcode = scraper.get_shortcode(details_url)

        location_data = None
        if location:
            location_data = scraper.get_location(location)

        return cls(
            image_url=result.find('img').get('src'),
            caption=result.find(attrs={'class': 'photo-description'}).get_text(
                strip=True
            ),
            location_name=location,
            details_url=result.find('a').get('href'),
            shortcode=shortcode,
            location_data=location_data
        )
