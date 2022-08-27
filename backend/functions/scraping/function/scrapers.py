import itertools
import random
import re
from abc import ABC, abstractmethod
from typing import Optional, List

import requests
from instaloader import Instaloader, Profile
from instaloader import Post as InstaPost
from bs4 import BeautifulSoup

from common.exceptions import InvalidUrlException
from common.constants import INSTA_SHORTCODE_REGEX
from common.utils import extract_insta_shortcode

from .constants import USER_AGENT_LIST
from .models import GramhirPost
from .providers import LocationProvider


class BaseScraper(ABC):
    @abstractmethod
    def get_last_post(self, username: str):
        pass

    @abstractmethod
    def get_post_from_url(self, url: str):
        pass

    @abstractmethod
    def get_last_posts(self, username: str, limit: int):
        pass


class InstagramScraper(BaseScraper):
    def __init__(self, client: Instaloader):
        self._client = client
        self._shortcode_regex = re.compile(INSTA_SHORTCODE_REGEX)

    @staticmethod
    def extract_shortcode(url: str) -> Optional[str]:
        return extract_insta_shortcode(url)

    def get_profile(self, username: str) -> Profile:
        return Profile.from_username(self._client.context, username)

    def get_last_post(self, username: str) -> InstaPost:
        profile = self.get_profile(username)
        post = next(profile.get_posts())
        return post

    def get_last_posts(self, username: str, limit: int) -> List[InstaPost]:
        profile = self.get_profile(username)
        post_iterator = profile.get_posts()
        if post_iterator.count <= limit:
            return list(post_iterator)
        return [post for post in itertools.islice(post_iterator, limit)]

    def get_post_from_url(self, url: str) -> InstaPost:
        shortcode = self.extract_shortcode(url)
        if not shortcode:
            raise InvalidUrlException('Cannot extract shortcode from provided URL')
        p = InstaPost.from_shortcode(self._client.context, shortcode)
        return p


class GramhirScraper(BaseScraper):
    _SEARCH_URL = 'https://gramhir.com/app/controllers/ajax.php'
    _PROFILE_URL = 'https://gramhir.com/profile/{username}/{gramhir_id}'

    def __init__(self, location_provider: Optional[LocationProvider] = None):
        self._session = requests.Session()
        self._session.headers.update(self._get_random_agent())
        self._location_provider = location_provider

    @staticmethod
    def _get_random_agent() -> dict:
        user_agent = random.choice(USER_AGENT_LIST)
        return {'User-Agent': user_agent}

    @staticmethod
    def _get_soup(data) -> BeautifulSoup:
        return BeautifulSoup(data, 'html.parser')

    def _search_user(self, username: str) -> str:
        """
        Get Gramhir internal user id
        """
        r = self._session.post(
            self._SEARCH_URL,
            data={'query': username, 'type': 'search_api'},
        )
        return r.text.split('/')[1]

    def _get_profile_url(self, username: str) -> str:
        gramhir_id = self._search_user(username)
        profile_url = self._PROFILE_URL.format(username=username, gramhir_id=gramhir_id)
        return profile_url

    def _get_posts(
        self, username: str, limit: Optional[int] = None
    ) -> List[GramhirPost]:
        r = self._session.get(self._get_profile_url(username))
        soup = self._get_soup(r.text)
        posts = soup.find_all(attrs={'class': 'box-photo'})

        if limit:
            posts = posts[:limit]

        return [GramhirPost.from_soup_result(p, self) for p in posts]

    def get_shortcode(self, details_url: str) -> str:
        r = self._session.get(details_url)
        details_page = r.text
        match = re.search(r'short_code\s=\s\"(.*)\"', details_page)
        return match.group(1)

    def get_location(self, location_name: str) -> Optional[dict]:
        if not self._location_provider:
            return None
        location = self._location_provider.search_location(location_name)
        if location:
            location = location['location']
            if location.get('lat') and location.get('lng'):
                return location
        return None

    def get_last_post(self, username: str):
        return self._get_posts(username, 1)[0]

    def get_last_posts(self, username: str, limit: int):
        return self._get_posts(username, limit)

    def get_post_from_url(self, url: str):
        raise NotImplementedError()
