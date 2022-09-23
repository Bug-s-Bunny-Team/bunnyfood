from typing import Union, Optional

from pydantic import BaseModel, Field

from db.models import GuideType


class ErrorResponse(BaseModel):
    detail: str


class User(BaseModel):
    username: str = Field(..., title='Username')

    class Config:
        orm_mode = True


class Location(BaseModel):
    id: int = Field(..., title='ID')
    name: str = Field(..., title='Name')
    description: str = Field(
        ..., title='Description', description='A brief description of the location'
    )
    lat: float = Field(
        0, title='Latitude', description='Latitude part of the coordinates'
    )
    long: float = Field(
        0, title='Longitude', description='Longitude part of the coordinates'
    )
    score: Optional[float] = Field(None, title='Score', ge=0, le=5)
    address: Optional[str] = Field(None, title='Address')
    maps_place_id: Optional[str] = Field(
        None, title='Maps Place ID', description='ID of the location on Google Maps'
    )

    class Config:
        orm_mode = True


class FollowedSocialProfile(BaseModel):
    username: str = Field(..., title='Username')


class SocialProfile(FollowedSocialProfile):
    id: int = Field(..., title='ID')
    followers_count: Optional[int] = Field(
        0,
        title='Followers count',
        description='Number of users following this profile',
    )

    class Config:
        orm_mode = True


class UserPreferences(BaseModel):
    default_guide_view: GuideType = Field(
        GuideType.MAP,
        title='Default guide view',
        description='Which type of map the user wants',
    )

    class Config:
        orm_mode = True
