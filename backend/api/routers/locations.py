from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import schemas
from api.dependencies import get_db

from db import models

router = APIRouter()


@router.get(
    '/locations',
    response_model=List[schemas.Location],
    response_model_exclude_unset=True,
)
def get_locations(db: Session = Depends(get_db)):
    return db.query(models.Location).all()


@router.get(
    '/locations/{location_id}',
    response_model=schemas.Location,
    response_model_exclude_unset=True,
)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(models.Location).filter_by(id=location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail='Location not found')
    return location
