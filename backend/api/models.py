from sqlalchemy import Column, Integer, String, Text, Float

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True)


class SocialProfile(Base):
    __tablename__ = 'socialprofiles'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True)


class UserPreferences(Base):
    __tablename__ = 'userpreferences'

    id = Column(Integer, primary_key=True, index=True)
    default_guide_view = Column(String(10), default='map')


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50))
    description = Column(Text)
    lat = Column(Float, default=0)
    long = Column(Float, default=0)
    score = Column(Float, nullable=True, default=None)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
