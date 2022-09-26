from typing import List

from fastapi import status, Depends, HTTPException, Response

from api import schemas
from api.crud.profiles import ProfilesCRUD
from api.dependencies import get_user, get_profiles_crud, get_username
from api.routers import APIRouter
from api.s4 import s4
from api.schemas import ErrorResponse
from api.utils import search_social_profile
from db import models

router = APIRouter()


@router.get(
    '/profiles/',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_profiles(
    unfollowed_only: bool = True,
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
    user: models.User = Depends(get_user),
):
    """
    Get all SocialProfiles. By default only unfollowed by the user.
    """
    if unfollowed_only:
        return profiles.get_all(user)
    return profiles.get_all()


@router.get(
    '/profiles/{profile_id}',
    response_model=schemas.SocialProfile,
    response_model_exclude_unset=True,
    responses={404: {'model': ErrorResponse}},
)
def get_profile_by_id(
    profile_id: int,
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
    _=Depends(get_username),
):
    """
    Get a SocialProfile by its ID
    """
    profile = profiles.get_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='SocialProfile not found'
        )
    return profile


@router.get(
    '/profiles/search/{profile_username}',
    response_model=schemas.SocialProfile,
    responses={
        200: {
            'description': 'SocialProfile exists and already added',
        },
        201: {
            'description': 'SocialProfile exists and has been added',
            'model': schemas.SocialProfile,
        },
        204: {'description': 'User is already following this SocialProfile'},
        404: {'model': ErrorResponse},
    },
)
def search_profile(
    profile_username: str,
    response: Response,
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
    user: models.User = Depends(get_user),
):
    """
    Search a SocialProfile by its username. If already existing, just return it.
    If new, start S4 on such profile and return it.
    """
    profile = profiles.get_by_username(profile_username)
    if not profile:
        if search_social_profile(profile_username):
            profile = profiles.create_profile(profile_username)
            s4.start(profile_username)
            response.status_code = status.HTTP_201_CREATED
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='SocialProfile not found'
            )
    if profile in user.followed_profiles:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return profile


@router.get(
    '/profiles/popular/{limit}',
    response_model=List[schemas.SocialProfile],
    responses={
        400: {
            'model': ErrorResponse,
            'description': 'Too many profiles requested',
        }
    },
)
def get_most_popular_profiles(
    limit: int,
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
    user: models.User = Depends(get_user),
):
    """
    Get the most followed SocialProfiles.
    If the number of popular profiles is less than specified, more will be added
    even if without any followers.
    """
    if limit > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Can provide at most 20 popular profiles',
        )

    results = profiles.get_most_popular(user, limit)
    if not results:
        # fallback to all profiles with limit if most popular is empty
        results = profiles.get_all(user, limit)
    if results_count := len(results) < limit:
        results = results + profiles.get_all(user, limit - results_count, results)
    return results


@router.get(
    '/followed/',
    response_model=List[schemas.SocialProfile],
    response_model_exclude_unset=True,
)
def get_followed_profiles(
    user: models.User = Depends(get_user),
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
):
    """
    Get all followed SocialProfiles by the user.
    """
    followed = profiles.get_user_followed(user)
    return followed


@router.post(
    '/followed/',
    response_model=schemas.SocialProfile,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
    responses={404: {'model': ErrorResponse}},
)
def follow_profile(
    profile: schemas.FollowedSocialProfile,
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
    user: models.User = Depends(get_user),
):
    """
    Follow a SocialProfile, by its username.
    """
    profile_username = profile.username
    profile = profiles.get_by_username(profile_username)

    if not profile:
        if search_social_profile(profile_username):
            profile = profiles.create_profile(profile_username)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='SocialProfile not found'
            )

    profiles.follow_profile(profile, user)
    return profile


@router.post('/followed/unfollow/', responses={404: {'model': ErrorResponse}})
def unfollow_profile(
    profile: schemas.FollowedSocialProfile,
    user: models.User = Depends(get_user),
    profiles: ProfilesCRUD = Depends(get_profiles_crud),
):
    """
    Unfollow a SocialProfile followed by the user.
    """
    db_profile = profiles.get_by_username(profile.username)
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='SocialProfile does not exist'
        )
    profiles.unfollow_profile(db_profile, user)
