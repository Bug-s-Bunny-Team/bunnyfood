from typing import Union, Any

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Base(BaseModel):
    id: Union[int, None] = None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Location(Base):
    name: str
    description: str
    lat: float = 0
    long: float = 0
    score: float = 0


class SocialProfile(Base):
    username: str
