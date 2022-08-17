from fastapi import APIRouter

from api.models import SocialProfile

router = APIRouter()


@router.get('/profiles')
def get_profiles():
    return [{'id': 1, 'username': 'someone'}]


@router.get('/profiles/{profile_id}')
def get_profile(profile_id: int):
    return {'id': profile_id, 'username': f'someone{profile_id}'}


@router.post('/profiles/')
def add_profile(profile: SocialProfile):
    username = profile.username
    print(username)
