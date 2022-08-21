from fastapi import FastAPI

from .routers import locations, profiles, preferences

app = FastAPI()

app.include_router(locations.router)
app.include_router(profiles.router)
app.include_router(preferences.router)
