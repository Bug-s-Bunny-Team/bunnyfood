from typing import List

from fastapi import APIRouter

from api.schemas import SocialProfile

router = APIRouter()


@router.get(
    '/profiles', response_model=List[SocialProfile], response_model_exclude_unset=True
)
def get_profiles():
    return [
        SocialProfile(id=1, username='someone1'),
        SocialProfile(id=2, username='someone2'),
    ]


@router.get(
    '/profiles/{profile_id}',
    response_model=SocialProfile,
    response_model_exclude_unset=True,
)
def get_profile(profile_id: int):
    return SocialProfile(id=profile_id, username=f'someone{profile_id}')


@router.post('/profiles/')
def add_profile(profile: SocialProfile):
    username = profile.username
    print(username)
