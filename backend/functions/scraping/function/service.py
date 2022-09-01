import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from common.service import BaseService
from db import models
from db.utils import get_or_create
from .download import Downloader
from .models import ScrapingEvent, ScrapedPost
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

    def _scrape_last_post(self, username: str) -> Optional[ScrapedPost]:
        print(f'getting last post for "{username}"')
        scraped_post = self._scraper.get_last_post(username)
        return scraped_post

    def _scrape_last_posts(self, username: str, limit: int) -> List[ScrapedPost]:
        print(f'getting last {limit} posts for "{username}"')
        scraped_posts = self._scraper.get_last_posts(username, limit)
        return scraped_posts

    def _get_profile(self, username: str) -> models.SocialProfile:
        profile = get_or_create(self._session, models.SocialProfile, username=username)
        return profile

    def _set_last_scraped(self, profile: models.SocialProfile):
        profile.last_scraped = datetime.datetime.now()
        self._session.add(profile)
        self._session.commit()

    def _process_posts(
        self, scraped_posts: List[ScrapedPost], profile: models.SocialProfile
    ) -> List[models.Post]:
        downloaded_posts = []

        for scraped in scraped_posts:
            if not scraped.has_valid_location:
                print('post has no valid location data, skipping')
            else:
                name = (
                    scraped.location_data.maps_name
                    if scraped.location_data.maps_name
                    else scraped.location_name
                )

                location = None
                if scraped.location_data.maps_place_id:
                    location = (
                        self._session.query(models.Location)
                        .filter_by(maps_place_id=scraped.location_data.maps_place_id)
                        .first()
                    )
                if not location:
                    location = get_or_create(
                        self._session,
                        models.Location,
                        name=name,
                        description=scraped.description,
                        lat=scraped.location_data.lat,
                        long=scraped.location_data.long,
                        address=scraped.location_data.address,
                        maps_place_id=scraped.location_data.maps_place_id,
                    )

                post, created = models.Post.from_scraped_post(
                    self._session, scraped, profile, location
                )

                if created:
                    key = self._download_post(post)
                    post.media_s3_key = key
                    self._session.add(post)
                    self._session.commit()
                    downloaded_posts.append(post)
                else:
                    print('post already in db, skipping download')

        return downloaded_posts

    def process_event(self, event: ScrapingEvent) -> dict:
        if event.posts_limit == 1:
            post = self._scrape_last_post(event.username)
            posts = [post] if post else []
        else:
            posts = self._scrape_last_posts(event.username, event.posts_limit)

        profile = self._get_profile(event.username)
        self._set_last_scraped(profile)

        if len(posts) > 0:
            downloaded_posts = self._process_posts(posts, profile)
            downloaded_posts = [{'id': p.id} for p in downloaded_posts]
            return {'posts_count': len(downloaded_posts), 'posts': downloaded_posts}
        else:
            return {'posts_count': 0, 'posts': []}
