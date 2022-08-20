from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from .jwt import JWTBearer, JWTAuthorizationCredentials

auth = JWTBearer()


async def get_username(
    credentials: JWTAuthorizationCredentials = Depends(auth),
) -> str:
    try:
        return credentials.claims['cognito:username']
    except KeyError:
        HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Username missing')
