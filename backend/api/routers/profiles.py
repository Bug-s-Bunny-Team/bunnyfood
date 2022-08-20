from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from api import schemas
from api.dependencies import get_db

from db import models

router = APIRouter()


@router.get(
    '/profiles',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_profiles(db: Session = Depends(get_db)):
    return db.query(models.SocialProfile).all()


@router.get(
    '/profiles/{profile_id}',
    response_model=schemas.SocialProfile,
    response_model_exclude_unset=True,
)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.SocialProfile).filter_by(id=profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail='SocialProfile not found')
    return profile


@router.get(
    '/profiles/popular/{limit}',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_most_popular_profiles(limit: int, db: Session = Depends(get_db)):
    if limit > 50:
        raise HTTPException(
            status_code=400, detail='Can provide at most 50 popular profiles'
        )
    return []


@router.get(
    '/profiles/followed',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_followed_profiles(db: Session = Depends(get_db)):
    return []


@router.post('/profiles/followed/', status_code=status.HTTP_201_CREATED)
def follow_profile(profile: schemas.SocialProfile, db: Session = Depends(get_db)):
    db_profile = db.models.SocialProfile(username=profile.username)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.delete(
    '/profiles/followed/',
)
def follow_profile(profile: schemas.SocialProfile, db: Session = Depends(get_db)):
    return {}
