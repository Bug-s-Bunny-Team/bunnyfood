import datetime
from enum import Enum, unique
from functools import cached_property
from typing import Set, Tuple, Optional

from peewee import (
    Model,
    CharField,
    TextField,
    ForeignKeyField,
    FloatField,
    IntegerField,
    DateTimeField
)

from . import db


@unique
class MediaType(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'


class BaseModel(Model):
    class Meta:
        database = db


class SocialProfile(BaseModel):
    username = CharField(unique=True, null=False)


class Location(BaseModel):
    insta_id = IntegerField()
    name = CharField(unique=True)
    lat = FloatField(default=0)
    long = FloatField(default=0)
    score = FloatField(null=True)

    @classmethod
    def from_instaloader_location(cls, location) -> Tuple['Location', bool]:
        return Location.get_or_create(
            # insta_id=location.id,
            insta_id=0,     # some ids causes an overflow, need to fix later
            name=location.name,
            lat=location.lat,
            long=location.lng,
        )


class Post(BaseModel):
    shortcode = CharField(unique=True)
    caption = TextField()
    social_profile = ForeignKeyField(SocialProfile, backref='posts', lazy_load=False)
    media_type = CharField(choices=[MediaType.IMAGE, MediaType.VIDEO])
    media_url = CharField(max_length=512)
    media_s3_key = CharField(null=True, unique=True)
    location = ForeignKeyField(Location, backref='posts', lazy_load=False, null=True)
    added = DateTimeField(default=datetime.datetime.now())

    @cached_property
    def media_filename(self) -> str:
        extension = 'mp4' if self.media_type == MediaType.VIDEO else 'jpg'
        return f'{self.shortcode}.{extension}'

    @cached_property
    def hashtags(self) -> Set[str]:
        tags = [tag.strip('#') for tag in self.caption.split() if tag.startswith('#')]
        return set(tags)

    @classmethod
    def from_instaloader_post(
        cls, insta_post, profile: SocialProfile, location: Optional[Location] = None
    ) -> Tuple['Post', bool]:
        if post := Post.get_or_none(shortcode=insta_post.shortcode):
            return post, False
        post = Post.create(
            shortcode=insta_post.shortcode,
            caption=insta_post.caption,
            media_url=insta_post.video_url if insta_post.is_video else insta_post.url,
            media_type=MediaType.VIDEO if insta_post.is_video else MediaType.IMAGE,
            social_profile=profile,
            location=location
        )
        return post, True


class PostScore(BaseModel):
    media_score = FloatField(default=0)
    caption_score = FloatField(default=0)
    post = ForeignKeyField(Post, backref='score', lazy_load=False, unique=True)
    created = DateTimeField(default=datetime.datetime.now())
