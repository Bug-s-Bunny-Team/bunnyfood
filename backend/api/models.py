from pydantic import BaseModel


class Location(BaseModel):
    name: str
    description: str


class SocialProfile(BaseModel):
    username: str
