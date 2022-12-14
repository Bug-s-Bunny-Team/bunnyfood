from enum import unique, Enum
from functools import cached_property
from typing import Tuple, Set

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    func,
    DateTime,
)
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import relationship, Session

from db import Base
from db.utils import gc_distance, get_or_create


@unique
class MediaType(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'


@unique
class GuideType(str, Enum):
    MAP = 'map'
    LIST = 'list'


profiles_users_association = Table(
    'profiles_users',
    Base.metadata,
    Column('left_id', ForeignKey('socialprofiles.id'), primary_key=True),
    Column('right_id', ForeignKey('users.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True)

    preferences = relationship('UserPreferences', back_populates='user', uselist=False)
    followed_profiles = relationship(
        'SocialProfile',
        secondary=profiles_users_association,
        back_populates='followers',
    )


class UserPreferences(Base):
    __tablename__ = 'userpreferences'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    default_guide_view = Column(String(10), default='map')

    user = relationship('User', back_populates='preferences', uselist=False)


class SocialProfile(Base):
    __tablename__ = 'socialprofiles'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True)
    last_scraped = Column(DateTime, nullable=True, default=None)

    posts = relationship('Post', back_populates='profile')
    followers = relationship(
        'User', secondary=profiles_users_association, back_populates='followed_profiles'
    )


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    lat = Column(Float, default=0)
    long = Column(Float, default=0)
    score = Column(Float, nullable=True, default=None)
    last_scored = Column(DateTime, nullable=True, default=None)
    address = Column(Text, nullable=True, default=None)
    maps_place_id = Column(String, nullable=True, default=None, unique=True)

    posts = relationship('Post', back_populates='location')

    @hybrid_method
    def distance(self, lat, lng):
        return gc_distance(lat, lng, self.lat, self.long)

    @distance.expression
    def distance(cls, lat, lng):
        return gc_distance(lat, lng, cls.lat, cls.long, math_lib=func)

    @classmethod
    def from_instaloader_location(cls, session: Session, location) -> 'Location':
        location = get_or_create(
            session,
            cls,
            name=location.name,
            lat=location.lat,
            long=location.lng,
            description='',
        )
        return location


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('socialprofiles.id'))
    location_id = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'))
    shortcode = Column(String, unique=True)
    caption = Column(Text)
    media_type = Column(String)
    media_url = Column(String)
    media_s3_key = Column(String, nullable=True, unique=True)
    score = Column(Float, nullable=True, default=None)

    profile = relationship('SocialProfile', back_populates='posts')
    location = relationship('Location', back_populates='posts')

    @cached_property
    def media_filename(self) -> str:
        extension = 'mp4' if self.media_type == MediaType.VIDEO else 'jpg'
        return f'{self.shortcode}.{extension}'

    @cached_property
    def hashtags(self) -> Set[str]:
        tags = [tag.strip('#') for tag in self.caption.split() if tag.startswith('#')]
        return set(tags)

    @classmethod
    def from_scraped_post(
        cls, session: Session, scraped_post, profile: SocialProfile, location: Location
    ) -> Tuple['Post', bool]:
        post = session.query(Post).filter_by(shortcode=scraped_post.shortcode).first()
        if post:
            return post, False
        post = Post(
            shortcode=scraped_post.shortcode,
            caption=scraped_post.caption,
            media_url=scraped_post.image_url,
            media_type=MediaType.IMAGE,
            profile=profile,
            location=location,
        )
        session.add(post)
        session.commit()
        session.refresh(post)
        return post, True


class GramhirProfiles(Base):
    __tablename__ = 'gramhirprofiles'

    gramhir_id = Column(String(length=20), primary_key=True)
    username = Column(String(length=50), primary_key=True)
