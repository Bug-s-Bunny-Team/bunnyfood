from typing import Union

from pydantic import BaseModel


class Base(BaseModel):
    id: Union[int, None] = None


class Location(Base):
    name: str
    description: str


class SocialProfile(Base):
    username: str
