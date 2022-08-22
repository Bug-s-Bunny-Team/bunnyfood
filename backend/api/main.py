from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_418_IM_A_TEAPOT

from . import API_TITLE, API_DESCRIPTION, __version__

from .routers import locations, profiles, preferences

app = FastAPI()

app.include_router(locations.router)
app.include_router(profiles.router)
app.include_router(preferences.router)


@app.get('/', status_code=HTTP_418_IM_A_TEAPOT)
def get_details():
    return {
        'title': API_TITLE,
        'version': __version__,
        'description': API_DESCRIPTION,
    }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=__version__,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
