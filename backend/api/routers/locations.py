from typing import List, Union

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import column
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
    only_from_followed: bool = True,
    lat: Union[float, None] = None,
    long: Union[float, None] = None,
    current_lat: Union[float, None] = None,
    current_long: Union[float, None] = None,
    radius: Union[int, None] = None,
    min_rating: Union[float, None] = None,
):
    locations = db.query(
        models.Location,
        models.Location.distance(
            lat=current_lat if current_lat else 0,
            lng=current_long if current_long else 0,
        ).label('distance'),
    )
    if min_rating:
        locations = locations.filter(models.Location.score >= min_rating)
    if lat and long:
        locations = locations.filter(
            models.Location.lat == lat, models.Location.long == long
        )
    if all([current_lat, current_long, radius]):
        # filter by radius from current location
        locations = locations.having(column('distance') <= radius).order_by('distance')
    if only_from_followed:
        posts = (
            db.query(models.Post.id)
            .join(models.SocialProfile)
            .filter(
                models.SocialProfile.id.in_(
                    [profile.id for profile in user.followed_profiles]
                )
            )
            .subquery()
        )
        locations = locations.join(models.Post).filter(models.Post.id.in_(posts))
    locations = locations.all()

    for idx, l in enumerate(locations):
        distance = locations[idx][1]
        locations[idx] = locations[idx][0]
        locations[idx].distance = distance

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
