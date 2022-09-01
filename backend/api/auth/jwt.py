import os
from typing import Dict, Optional, List

import requests
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

__all__ = ['JWKS', 'JWTBearer', 'JWTBearerDev']

JWK = Dict[str, str]


class JWTAuthorizationCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, str]
    signature: str
    message: str


class JWKS(BaseModel):
    keys: List[JWK] = []

    @classmethod
    def from_keys_json(cls, keys_url: Optional[str] = None):
        if not keys_url:
            keys_url = (
                f"https://cognito-idp.{os.environ.get('REGION_NAME')}.amazonaws.com/"
                f"{os.environ.get('COGNITO_POOL_ID')}/.well-known/jwks.json"
            )
        data = requests.get(keys_url)
        return cls.parse_obj(data.json())


class JWTBearer(HTTPBearer):
    def __init__(self, jwks: JWKS, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

        self.kid_to_jwk = {jwk['kid']: jwk for jwk in jwks.keys}

    def verify_jwk_token(self, jwt_credentials: JWTAuthorizationCredentials) -> bool:
        try:
            public_key = self.kid_to_jwk[jwt_credentials.header['kid']]
        except KeyError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail='JWK public key not found'
            )

        key = jwk.construct(public_key)
        decoded_signature = base64url_decode(jwt_credentials.signature.encode())

        return key.verify(jwt_credentials.message.encode(), decoded_signature)

    async def __call__(self, request: Request) -> Optional[JWTAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail='Wrong authentication method'
                )

            jwt_token = credentials.credentials

            message, signature = jwt_token.rsplit('.', 1)

            try:
                jwt_credentials = JWTAuthorizationCredentials(
                    jwt_token=jwt_token,
                    header=jwt.get_unverified_header(jwt_token),
                    claims=jwt.get_unverified_claims(jwt_token),
                    signature=signature,
                    message=message,
                )
            except JWTError:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail='JWK invalid'
                )

            if not self.verify_jwk_token(jwt_credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail='JWK invalid'
                )

            return jwt_credentials


class JWTBearerDev(JWTBearer):
    """
    Like JWTBearer, but doesn't actually verify the token. Only for dev purposes.
    """

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error, jwks=JWKS())

    def verify_jwk_token(self, jwt_credentials: JWTAuthorizationCredentials) -> bool:
        return True
