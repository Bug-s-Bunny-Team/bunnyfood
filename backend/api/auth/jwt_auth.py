import os

import requests
from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from .jwt import JWKS, JWTBearer, JWTAuthorizationCredentials

COGNITO_REGION = 'eu-central-1'
COGNITO_POOL_ID = os.environ.get('COGNITO_POOL_ID', 'eu-central-1_vzltHv2mZ')

jwks = JWKS.parse_obj(
    requests.get(
        f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/'
        f'{COGNITO_POOL_ID}/.well-known/jwks.json'
    ).json()
)

auth = JWTBearer(jwks)


async def get_current_user(
    credentials: JWTAuthorizationCredentials = Depends(auth),
) -> str:
    try:
        return credentials.claims['cognito:username']
    except KeyError:
        HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Username missing')
