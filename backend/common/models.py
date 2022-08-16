from pydantic import BaseModel, Json
from typing import Literal, Optional


class LambdaEvent(BaseModel):
    pass


class Request(LambdaEvent):
    resource: str
    path: str
    httpMethod: Literal['GET', 'POST']
    body: Optional[Json] = None

    class Config:
        extra = 'allow'
