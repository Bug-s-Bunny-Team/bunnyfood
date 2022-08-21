from enum import unique, Enum

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text, Float, func
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import relationship

from db import Base
from db.utils import gc_distance


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

    posts = relationship('Post', back_populates='profile')
    followers = relationship(
        'User', secondary=profiles_users_association, back_populates='followed_profiles'
    )


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), unique=True)
    description = Column(Text)
    lat = Column(Float, default=0)
    long = Column(Float, default=0)
    score = Column(Float, nullable=True, default=None)

    posts = relationship('Post', back_populates='location')

    @hybrid_method
    def distance(self, lat, lng):
        return gc_distance(lat, lng, self.lat, self.long)

    @distance.expression
    def distance(cls, lat, lng):
        return gc_distance(lat, lng, cls.lat, cls.long, math_lib=func)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('socialprofiles.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    profile = relationship('SocialProfile', back_populates='posts')
    location = relationship('Location', back_populates='posts')
