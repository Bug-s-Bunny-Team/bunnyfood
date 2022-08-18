from fastapi import FastAPI

from .routers import locations, profiles


app = FastAPI()

app.include_router(locations.router)
app.include_router(profiles.router)
