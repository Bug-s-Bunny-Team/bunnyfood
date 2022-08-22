from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import func, column
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from api import schemas
from api.dependencies import get_db, get_user
from api.utils import flatten_results

from db import models
from db.models import profiles_users_association
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
def get_profile_by_id(
    profile_id: int,
    db: Session = Depends(get_db),
):
    profile = db.query(models.SocialProfile).filter_by(id=profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail='SocialProfile not found'
        )
    return profile


@router.get(
    '/profiles/search/{profile_username}',
    response_model=schemas.SocialProfile,
    response_model_exclude_unset=True,
)
def get_profile_by_username(
    profile_username: str,
    db: Session = Depends(get_db),
):
    profile = db.query(models.SocialProfile).filter_by(username=profile_username).first()
    if not profile:
        # TODO: check if an actual social profile exists
        exists = False
        if exists:
            profile = models.SocialProfile(username=profile_username)
        else:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail='SocialProfile not found'
            )
    return profile


@router.get(
    '/profiles/popular/{limit}',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_most_popular_profiles(limit: int, db: Session = Depends(get_db)):
    if limit > 20:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Can provide at most 20 popular profiles',
        )

    profiles = (
        db.query(
            models.SocialProfile,
            func.count(profiles_users_association.c.right_id).label('followers_count'),
        )
        .join(profiles_users_association)
        .group_by(models.SocialProfile)
        .order_by(column('followers_count').desc())
        .all()
    )

    profiles = flatten_results(profiles, 'followers_count')

    return profiles


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
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail='SocialProfile does not exist'
        )
    user.followed_profiles.remove(db_profile)
    db.commit()
