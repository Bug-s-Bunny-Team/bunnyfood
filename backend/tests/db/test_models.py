from dataclasses import dataclass
from typing import Optional

import pytest
from instaloader import PostLocation

from db import db
from db.models import SocialProfile, Post, MediaType, Location
from db.utils import init_db, create_all_tables


@dataclass
class DummyInstaPost:
    shortcode: str
    caption: str
    url: Optional[str] = None
    video_url: Optional[str] = None

    @property
    def is_video(self) -> bool:
        return self.video_url is not None


@pytest.fixture
def transaction():
    init_db('user', 'password', '172.18.0.10', 'poc_test')
    with db.transaction() as txn:
        create_all_tables()
        yield txn
        txn.rollback()


@pytest.fixture
def profile() -> SocialProfile:
    return SocialProfile(username='testuser123')


@pytest.fixture
def post(profile) -> Post:
    return Post(
        shortcode='Cef7VMLloOP',
        social_profile=profile,
        media_type='image',
        media_url='https://instagram.fvce2-1.fna.fbcdn.net/v/dkfjgbndfjgbdfgsdfnsdf',
        caption='Great stuff #yum #friends',
    )


def test_create_profile(transaction, profile):
    profile.save()


def test_create_post(transaction, profile, post):
    profile.save()
    post.save()


def test_post_hashtags(post):
    hashtags = post.hashtags
    for expected in ['yum', 'friends']:
        assert expected in hashtags


def test_post_media_filename(post):
    assert post.media_filename == 'Cef7VMLloOP.jpg'


def test_media_type():
    assert MediaType('image') == MediaType.IMAGE
    assert MediaType('video') == MediaType.VIDEO
    assert MediaType['IMAGE'] == MediaType.IMAGE
    assert MediaType['VIDEO'] == MediaType.VIDEO


def test_create_from_instaloader_post(transaction, profile):
    profile.save()
    insta_post = DummyInstaPost(
        shortcode='Cef7VMLloOP',
        caption='A caption',
        url='https://instagram.fvce2-1.fna.fbcdn.net/v/dkfjgbndfjgbdfgsdfnsdf',
    )
    post, created = Post.from_instaloader_post(insta_post, profile)
    assert created
    assert post.media_type == MediaType.IMAGE


def test_create_from_instaloader_location(transaction):
    insta_location = PostLocation(
        123456, 'Random place', 'random-place', True, 40.0, 20.0
    )
    location, created = Location.from_instaloader_location(insta_location)
    assert created
    assert location.insta_id == 123456
