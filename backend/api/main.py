from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_418_IM_A_TEAPOT

from . import API_TITLE, API_DESCRIPTION, ENV, PREFIX, __version__
from .routers import locations, profiles, preferences

app = FastAPI(
    docs_url=f'{PREFIX}/docs',
    redoc_url=f'{PREFIX}/redoc',
    openapi_url=f'{PREFIX}/openapi.json',
)

app.include_router(locations.router)
app.include_router(profiles.router)
app.include_router(preferences.router)


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


@app.get(f'{PREFIX}/', status_code=HTTP_418_IM_A_TEAPOT, include_in_schema=False)
def get_details():
    return {
        'title': API_TITLE,
        'version': __version__,
        'description': API_DESCRIPTION,
        'env': ENV,
    }
