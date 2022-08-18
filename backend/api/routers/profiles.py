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


@router.post(
    '/profiles/',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_db)],
)
def add_profile(profile: schemas.SocialProfile):
    p, created = models.SocialProfile.get_or_create(username=profile.username)
    return p
