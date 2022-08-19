from typing import List

from fastapi import APIRouter, status, Depends, HTTPException

from api import schemas
from api.db import get_db
from db import models

router = APIRouter()


@router.get(
    '/profiles',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
    dependencies=[Depends(get_db)],
)
def get_profiles():
    return list(models.SocialProfile.select())


@router.get(
    '/profiles/{profile_id}',
    response_model=schemas.SocialProfile,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_db)],
)
def get_profile(profile_id: int):
    profile = models.SocialProfile.get_or_none(models.SocialProfile.id == profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail='SocialProfile not found')
    return profile


@router.get(
    '/profiles/popular/{limit}',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
    dependencies=[Depends(get_db)],
)
def get_most_popular_profiles(limit: int):
    if limit > 50:
        raise HTTPException(
            status_code=400, detail='Can provide at most 50 popular profiles'
        )
    return []


@router.get(
    '/profiles/followed',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
    dependencies=[Depends(get_db)],
)
def get_followed_profiles():
    return []


@router.post(
    '/profiles/followed/',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_db)],
)
def follow_profile(profile: schemas.SocialProfile):
    p, created = models.SocialProfile.get_or_create(username=profile.username)
    return p


@router.delete(
    '/profiles/followed/',
    dependencies=[Depends(get_db)],
)
def follow_profile(profile: schemas.SocialProfile):
    return {}
