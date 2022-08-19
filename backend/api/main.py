from fastapi import FastAPI

from .routers import locations, profiles, preferences
# from .auth.jwt_auth import jwks
# from .auth.jwt import JWTBearer

app = FastAPI()
# auth = JWTBearer(jwks)

app.include_router(locations.router)
app.include_router(profiles.router)
app.include_router(preferences.router)
