from dataclasses import dataclass
from typing import Optional

from common.models import LambdaEvent


class ScrapingEvent(LambdaEvent):
    username: str
    posts_limit: int = 6


@dataclass
class LocationData:
    lat: float
    long: float


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
