from typing import Optional

from pydantic import validator, root_validator

from common.models import LambdaEvent


class ScrapingEvent(LambdaEvent):
    username: Optional[str] = None
    url: Optional[str] = None

    @validator('url', always=True)
    def mutually_exclusive(cls, v, values):
        if values['username'] is not None and v:
            raise ValueError('"username" and "url" are mutually exclusive')
        return v

    @root_validator()
    def check_required(cls, values):
        if (values.get('username') is None) and (values.get('url') is None):
            raise ValueError('either "username" or "url" is required')
        return values
