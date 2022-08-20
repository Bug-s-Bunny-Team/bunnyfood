from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import db.models
from api import schemas, models
from api.dependencies import get_db

router = APIRouter()


@router.get(
    '/locations',
    response_model=List[schemas.Location],
    response_model_exclude_unset=True,
)
def get_locations(db: Session = Depends(get_db)):
    return db.query(db.models.Location).all()


@router.get(
    '/locations/{location_id}',
    response_model=schemas.Location,
    response_model_exclude_unset=True
)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(db.models.Location).filter_by(id=location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail='Location not found')
    return location
