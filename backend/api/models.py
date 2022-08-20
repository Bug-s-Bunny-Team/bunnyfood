from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from .database import Base

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

    preferences = relationship('UserPreferences', back_populates='user')
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


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('socialprofiles.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    profile = relationship('SocialProfile', back_populates='posts')
    location = relationship('Location', back_populates='posts')
