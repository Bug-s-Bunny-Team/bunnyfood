import re
from abc import ABC, abstractmethod
from typing import Optional

from instaloader import Instaloader, Profile
from instaloader import Post as InstaPost

from common.exceptions import InvalidUrlException
from common.constants import INSTA_SHORTCODE_REGEX
from common.utils import extract_insta_shortcode


class BaseScraper(ABC):
    @abstractmethod
    def get_last_post(self, username: str):
        pass

    @abstractmethod
    def get_post_from_url(self, url: str):
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

    def get_post_from_url(self, url: str) -> InstaPost:
        shortcode = self.extract_shortcode(url)
        if not shortcode:
            raise InvalidUrlException('Cannot extract shortcode from provided URL')
        p = InstaPost.from_shortcode(self._client.context, shortcode)
        return p
