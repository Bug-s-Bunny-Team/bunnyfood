from enum import Enum
from dataclasses import dataclass
from typing import Optional

from common.models import LambdaEvent


class ScraperType(str, Enum):
    RANDOM = 'RANDOM'
    GRAMHIR = 'GRAMHIR'
    PICUKI = 'PICUKI'


class ScrapingEvent(LambdaEvent):
    username: str
    posts_limit: int = 6
    scraper: ScraperType = ScraperType.RANDOM


@dataclass
class LocationData:
    lat: float
    long: float
    address: Optional[str] = None
    maps_name: Optional[str] = None
    maps_place_id: Optional[str] = None


@dataclass
class ScrapedPost:
    shortcode: str
    image_url: str
    caption: str
    description: str
    location_name: Optional[str] = None
    location_data: Optional[LocationData] = None

    @property
    def has_location(self) -> bool:
        return all([self.location_name, self.location_data])
