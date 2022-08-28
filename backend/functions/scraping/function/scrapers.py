import random
import re
from abc import ABC, abstractmethod
from typing import Optional, List

import requests
from bs4 import BeautifulSoup, Tag
from sqlalchemy.orm import Session

from db import models
from .constants import USER_AGENT_LIST
from .models import ScrapedPost, LocationData
from .providers import BaseLocationProvider


class BaseScraper(ABC):
    def __init__(self, location_provider: Optional[BaseLocationProvider] = None):
        self._location_provider = location_provider

    def _get_location_data(self, query: str) -> Optional[LocationData]:
        if not self._location_provider:
            return None
        return self._location_provider.search_location(query)

    @abstractmethod
    def get_last_post(self, username: str) -> Optional[ScrapedPost]:
        pass

    @abstractmethod
    def get_last_posts(self, username: str, limit: int) -> List[ScrapedPost]:
        pass


class SoupScraper(BaseScraper, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rsession = requests.Session()
        self._set_random_agent()

    @staticmethod
    def _get_random_agent() -> dict:
        user_agent = random.choice(USER_AGENT_LIST)
        return {'User-Agent': user_agent}

    @staticmethod
    def _get_soup(data) -> BeautifulSoup:
        return BeautifulSoup(data, 'html.parser')

    def _set_random_agent(self):
        self._rsession.headers.update(self._get_random_agent())


class GramhirScraper(SoupScraper):
    _SEARCH_URL = 'https://gramhir.com/app/controllers/ajax.php'
    _PROFILE_URL = 'https://gramhir.com/profile/{username}/{gramhir_id}'

    def __init__(self, session: Session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = session

    def _get_profile_internal_id(self, username: str) -> str:
        cache = (
            self._session.query(models.GramhirProfiles)
            .filter_by(username=username)
            .first()
        )
        if not cache:
            r = self._rsession.post(
                self._SEARCH_URL,
                data={'query': username, 'type': 'search_api'},
            )
            gramhir_id = r.text.split('/')[1]
            cache = models.GramhirProfiles(gramhir_id=gramhir_id, username=username)
            self._session.add(cache)
            self._session.commit()
        else:
            gramhir_id = cache.gramhir_id
        return gramhir_id

    def _get_profile_url(self, username: str) -> str:
        gramhir_id = self._get_profile_internal_id(username)
        profile_url = self._PROFILE_URL.format(username=username, gramhir_id=gramhir_id)
        return profile_url

    def _get_shortcode(self, details_url: str) -> str:
        r = self._rsession.get(details_url)
        details_page = r.text
        match = re.search(r'short_code\s=\s\"(.*)\"', details_page)
        return match.group(1)

    def _extract_post_data(self, post_result: Tag) -> ScrapedPost:
        location_name = post_result.find(attrs={'class': 'photo-location'}).get_text(
            strip=True
        )
        location_name = location_name if location_name else None

        location_data = None
        if location_name:
            location_data = self._get_location_data(location_name)

        details_url = post_result.find('a').get('href')
        shortcode = self._get_shortcode(details_url)

        return ScrapedPost(
            image_url=post_result.find('img').get('src'),
            caption=post_result.find(attrs={'class': 'photo-description'}).get_text(
                strip=True
            ),
            description='',
            location_name=location_name,
            location_data=location_data,
            shortcode=shortcode,
        )

    def _get_posts(
        self, username: str, limit: Optional[int] = None
    ) -> List[ScrapedPost]:
        r = self._rsession.get(self._get_profile_url(username))
        soup = self._get_soup(r.text)
        posts = soup.find_all(attrs={'class': 'box-photo'})

        if limit:
            posts = posts[:limit]

        scraped_posts = []
        for p in posts:
            scraped_posts.append(self._extract_post_data(p))

        return scraped_posts

    def get_last_post(self, username: str) -> Optional[ScrapedPost]:
        return self._get_posts(username, 1)[0]

    def get_last_posts(self, username: str, limit: int) -> List[ScrapedPost]:
        return self._get_posts(username, limit)


class PicukiScraper(GramhirScraper):
    """
    Seems to be te same as Gramhir, except for the profile url not requiring an internal id
    """

    _PROFILE_URL = 'https://picuki.com/profile/{username}'

    def __init__(self, *args, **kwargs):
        super().__init__(session=None, *args, **kwargs)

    def _get_profile_internal_id(self, username: str) -> str:
        raise NotImplementedError()

    def _get_profile_url(self, username: str) -> str:
        return self._PROFILE_URL.format(username=username)
