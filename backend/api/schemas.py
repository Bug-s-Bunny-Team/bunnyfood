from typing import Union

from pydantic import BaseModel


class Base(BaseModel):
    id: Union[int, None] = None


class Location(Base):
    name: str
    description: str
    lat: float = 0
    long: float = 0
    score: float = 0


class SocialProfile(Base):
    username: str
