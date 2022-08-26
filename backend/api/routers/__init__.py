from fastapi import APIRouter as BaseRouter

from api import ENV


class APIRouter(BaseRouter):
    def __init__(self):
        prefix = '/api' if ENV == 'prod' else ''
        super().__init__(prefix=prefix)
