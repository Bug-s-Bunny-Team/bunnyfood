from typing import List, Union

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from api import schemas
from api.dependencies import get_db, get_user

from db import models

router = APIRouter()


@router.get(
    '/locations/',
    response_model=List[schemas.Location],
    response_model_exclude_unset=True,
)
def get_locations(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user),
    only_followed: bool = True,
    lat: Union[float, None] = None,
    long: Union[float, None] = None,
    radius: int = 0,
    min_rating: Union[float, None] = None,
):
    locations = db.query(models.Location)
    if min_rating:
        locations = locations.filter(models.Location.score >= min_rating)
    if lat and long:
        locations = locations.filter(models.Location.lat == lat, models.Location.long == long)
    locations = locations.all()
    return locations


@router.get(
    '/locations/{location_id}',
    response_model=schemas.Location,
    response_model_exclude_unset=True,
)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(models.Location).filter_by(id=location_id).first()
    if not location:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Location not found')
    return location
