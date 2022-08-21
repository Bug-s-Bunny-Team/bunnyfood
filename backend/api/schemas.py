from pydantic import BaseModel

from db.models import GuideType


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class Location(BaseModel):
    name: str
    description: str
    lat: float = 0
    long: float = 0
    score: float = 0

    class Config:
        orm_mode = True


class FollowedSocialProfile(BaseModel):
    username: str


class SocialProfile(FollowedSocialProfile):
    class Config:
        orm_mode = True


class UserPreferences(BaseModel):
    default_guide_view: GuideType = GuideType.MAP

    class Config:
        orm_mode = True
