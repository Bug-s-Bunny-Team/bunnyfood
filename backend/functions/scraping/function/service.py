from typing import List, Optional

from instaloader import Post as InstaPost
from sqlalchemy.orm import Session

from common.service import BaseService
from db import models
from db.utils import get_or_create
from .download import Downloader
from .models import ScrapingEvent, GramhirPost
from .scrapers import BaseScraper


class ScrapingService(BaseService):
    def __init__(self, scraper: BaseScraper, downloader: Downloader, session: Session):
        self._scraper = scraper
        self._session = session
        self._downloader = downloader

    def _download_post(self, post: models.Post) -> str:
        print(f'downloading post "{post.shortcode}"')
        key = self._downloader.download_and_save_post(post)
        return key

    # def _scrape_last_post(self, username: str) -> InstaPost:
    def _scrape_last_post(self, username: str) -> GramhirPost:
        print(f'getting last post for "{username}"')
        insta_post = self._scraper.get_last_post(username)
        return insta_post

    # def _scrape_last_posts(self, username: str, limit: int) -> List[InstaPost]:
    def _scrape_last_posts(self, username: str, limit: int) -> List[GramhirPost]:
        print(f'getting last {limit} posts for "{username}"')
        insta_posts = self._scraper.get_last_posts(username, limit)
        return insta_posts

    def _scrape_url(self, url: str) -> InstaPost:
        print(f'getting post from url')
        insta_post = self._scraper.get_post_from_url(url)
        return insta_post

    # def _extract_location(self, post: InstaPost) -> Optional[models.Location]:
    #     insta_location = post.location
    #     if not insta_location:
    #         print('post has no location data, skipping')
    #         return None
    #     location = models.Location.from_instaloader_location(
    #         self._session, insta_location
    #     )
    #     return location

    # def process_event(self, event: ScrapingEvent) -> dict:
    #     posts = self._scrape_last_posts(event.username, event.posts_limit)
    #
    #     if len(posts) > 0:
    #         profile = get_or_create(
    #             self._session, models.SocialProfile, username=event.username
    #         )
    #         downloaded_posts = []
    #
    #         for insta_post in posts:
    #             location = self._extract_location(insta_post)
    #             if not location:
    #                 print('post has no location data, skipping')
    #             else:
    #                 post, created = models.Post.from_instaloader_post(
    #                     self._session, insta_post, profile, location
    #                 )
    #
    #                 if created:
    #                     key = self._download_post(post)
    #                     post.media_s3_key = key
    #                     self._session.add(post)
    #                     self._session.commit()
    #                     downloaded_posts.append(post)
    #                 else:
    #                     print('post already in db, skipping download')
    #         downloaded_posts = [
    #             {'id': post.id, 'media_s3_key': post.media_s3_key}
    #             for post in downloaded_posts
    #         ]
    #         return {'posts_count': len(downloaded_posts), 'posts': downloaded_posts}
    #     else:
    #         return {'posts_count': 0}

    def process_event(self, event: ScrapingEvent) -> dict:
        posts = self._scrape_last_posts(event.username, event.posts_limit)

        if len(posts) > 0:
            profile = get_or_create(
                self._session, models.SocialProfile, username=event.username
            )
            downloaded_posts = []

            for insta_post in posts:
                if not insta_post.location_data:
                    print('post has no location data, skipping')
                else:
                    location = get_or_create(
                        self._session,
                        models.Location,
                        name=insta_post.location_name,
                        description='',
                        lat=insta_post.location_data['lat'],
                        long=insta_post.location_data['long'],
                    )
                    post, created = models.Post.from_gramhir_post(
                        self._session, insta_post, profile, location
                    )

                    if created:
                        key = self._download_post(post)
                        post.media_s3_key = key
                        self._session.add(post)
                        self._session.commit()
                        downloaded_posts.append(post)
                    else:
                        print('post already in db, skipping download')

            downloaded_posts = [
                {'id': post.id, 'media_s3_key': post.media_s3_key}
                for post in downloaded_posts
            ]

            return {'posts_count': len(downloaded_posts), 'posts': downloaded_posts}

        else:
            return {'posts_count': 0}
