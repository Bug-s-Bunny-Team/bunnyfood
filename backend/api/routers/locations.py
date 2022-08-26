from typing import List, Optional

from fastapi import HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND

from api import schemas
from api.crud.locations import LocationsCRUD
from api.dependencies import get_user, get_locations_crud
from api.routers import APIRouter
from db import models

router = APIRouter()


@router.get(
    '/locations/',
    response_model=List[schemas.Location],
    response_model_exclude_unset=True,
)
def get_locations(
    only_from_followed: bool = True,
    lat: Optional[float] = None,
    long: Optional[float] = None,
    current_lat: Optional[float] = None,
    current_long: Optional[float] = None,
    radius: Optional[int] = None,
    min_rating: Optional[float] = None,
    user: models.User = Depends(get_user),
    locations: LocationsCRUD = Depends(get_locations_crud),
):
    return locations.get_from_filters(
        user,
        only_from_followed,
        lat,
        long,
        current_lat,
        current_long,
        radius,
        min_rating,
    )


@router.get(
    '/locations/{location_id}',
    response_model=schemas.Location,
    response_model_exclude_unset=True,
)
def get_location(
    location_id: int,
    locations: LocationsCRUD = Depends(get_locations_crud),
):
    location = locations.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Location not found')
    return location
