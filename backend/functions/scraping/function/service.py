import json
import os

import boto3
from instaloader import Post as InstaPost

from common.utils import create_error_response
from db import models, SessionLocal
from db.utils import get_or_create
from .download import download_and_save_post
from .models import ScrapingEvent
from .scrapers import InstagramScraper


class ScrapingService:
    def __init__(self, scraper: InstagramScraper):
        self._scraper = scraper
        self._sns_topic = boto3.resource('sns').Topic(os.environ['SNS_SCORING_TOPIC'])
        self._session = SessionLocal()

    def _get_success_response(self, post: models.Post):
        return {
            'statusCode': 200,
            'body': json.dumps(
                {'post': {'shortcode': post.shortcode, 'media_url': post.media_url}}
            ),
        }

    def _download_post(self, post: models.Post) -> str:
        print(f'downloading post "{post.shortcode}"')
        key = download_and_save_post(post)
        return key

    def _scrape_last_post(self, username: str) -> InstaPost:
        print(f'getting last post for "{username}"')
        insta_post = self._scraper.get_last_post(username)
        return insta_post

    def _scrape_url(self, url: str) -> InstaPost:
        print(f'getting post from url')
        insta_post = self._scraper.get_post_from_url(url)
        return insta_post

    def process_event(self, event: ScrapingEvent) -> dict:
        insta_post = self._scrape_last_post(event.username)

        profile = get_or_create(
            self._session, models.SocialProfile, username=insta_post.owner_username
        )

        insta_location = insta_post.location
        if not insta_location:
            print('post has no location data, skipping')
            return create_error_response('Post does not have location data')

        location = models.Location.from_instaloader_location(
            self._session, insta_location
        )
        post, created = models.Post.from_instaloader_post(self._session, insta_post, profile, location)

        if created:
            key = self._download_post(post)
            post.media_s3_key = key
            self._session.add(post)
            self._session.commit()
        else:
            print('post already in db, skipping download')

        print('publishing scoring message to topic')
        self._sns_topic.publish(Message=json.dumps({'post_id': post.id}))

        return self._get_success_response(post)
