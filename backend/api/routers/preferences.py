from fastapi import APIRouter, Depends, HTTPException

from api import schemas
# from api.auth.jwt_auth import get_current_user
from api.dependencies import get_db
from api.schemas import GuideType
from db import models

router = APIRouter()


@router.get(
    # '/preferences',
    '/preferences/{username}',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_db)],
)
# def get_user_prefs(username: str = Depends(get_current_user)):
def get_user_prefs(username: str):
    user = models.User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    prefs, _ = models.UserPreferences.get_or_create(user=user)
    return prefs
