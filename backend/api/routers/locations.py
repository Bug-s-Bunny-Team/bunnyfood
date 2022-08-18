from typing import List

from fastapi import APIRouter, HTTPException, Depends

from api import schemas
from api.db import get_db
from db import models

router = APIRouter()


@router.get(
    '/locations',
    response_model=List[schemas.Location],
    response_model_exclude_unset=True,
    dependencies=[Depends(get_db)],
)
def get_locations():
    return list(models.Location.select())


@router.get(
    '/locations/{location_id}',
    response_model=schemas.Location,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_db)],
)
def get_location(location_id: int):
    location = models.Location.get_or_none(models.Location.id == location_id)
    if not location:
        raise HTTPException(status_code=404, detail='Location not found')
    return location
