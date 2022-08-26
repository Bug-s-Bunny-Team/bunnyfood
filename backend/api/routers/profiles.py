from typing import List

from fastapi import status, Depends, HTTPException, Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from api import schemas
from api.crud.profiles import ProfilesCRUD
from api.dependencies import get_user, get_profiles_crud
from api.routers import APIRouter
from api.utils import search_social_profile
from db import models

router = APIRouter()


@router.get(
    '/profiles/',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_profiles(
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
):
    return profiles.get_all()


@router.get(
    '/profiles/{profile_id}',
    response_model=schemas.SocialProfile,
    response_model_exclude_unset=True,
)
def get_profile_by_id(
    profile_id: int,
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
):
    profile = profiles.get_by_id(profile_id)
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
    response: Response,
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
):
    profile = profiles.get_by_username(profile_username)
    if not profile:
        if search_social_profile(profile_username):
            profile = profiles.create_profile(profile_username)
            response.status_code = HTTP_201_CREATED
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
def get_most_popular_profiles(
    limit: int, profiles: ProfilesCRUD = Depends(get_profiles_crud)
):
    if limit > 20:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Can provide at most 20 popular profiles',
        )

    return profiles.get_most_popular(limit)


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
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
    user: models.User = Depends(get_user),
):
    profiles.follow_profile(profile, user)


@router.post(
    '/followed/unfollow/',
)
def unfollow_profile(
    profile: schemas.FollowedSocialProfile,
    user: models.User = Depends(get_user),
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
):
    db_profile = profiles.get_by_username(profile.username)
    if not db_profile:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail='SocialProfile does not exist'
        )
    profiles.unfollow_profile(db_profile, user)
