from fastapi import APIRouter as BaseRouter

from api import PREFIX


class APIRouter(BaseRouter):
    def __init__(self):
        super().__init__(prefix=PREFIX)
