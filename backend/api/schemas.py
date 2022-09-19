from typing import Union, Optional

from pydantic import BaseModel

from db.models import GuideType


class ErrorResponse(BaseModel):
    detail: str


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class Location(BaseModel):
    id: int
    name: str
    description: str
    lat: float = 0
    long: float = 0
    score: Optional[float] = None
    address: Optional[str] = None
    maps_place_id: Optional[str] = None

    class Config:
        orm_mode = True


class FollowedSocialProfile(BaseModel):
    username: str


class SocialProfile(FollowedSocialProfile):
    id: int
    followers_count: Union[int, None] = 0

    class Config:
        orm_mode = True


class UserPreferences(BaseModel):
    default_guide_view: GuideType = GuideType.MAP

    class Config:
        orm_mode = True
