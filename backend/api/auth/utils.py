from api import ENV
from api.auth.jwt import JWKS, JWTBearer, JWTBearerDev


def get_auth():
    if ENV == 'prod':
        jwks = JWKS.from_keys_json()
        auth = JWTBearer(jwks)
    else:
        auth = JWTBearerDev()
    return auth
