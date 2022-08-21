from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from api import schemas
from api.dependencies import get_db, get_user

from db import models
from db.utils import get_or_create

router = APIRouter()


@router.get(
    '/profiles/',
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
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):
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
    '/followed/',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_followed_profiles(user: models.User = Depends(get_user)):
    followed = user.followed_profiles
    return followed


@router.post(
    '/followed/',
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def follow_profile(
    profile: schemas.FollowedSocialProfile,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user),
):
    db_profile = get_or_create(db, models.SocialProfile, username=profile.username)
    user.followed_profiles.append(db_profile)
    db.add(user)
    db.commit()


@router.post(
    '/followed/unfollow/',
)
def unfollow_profile(
    profile: schemas.FollowedSocialProfile,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user),
):
    db_profile = (
        db.query(models.SocialProfile).filter_by(username=profile.username).first()
    )
    if not db_profile:
        raise HTTPException(status_code=404, detail='SocialProfile does not exist')
    user.followed_profiles.remove(db_profile)
    db.commit()
