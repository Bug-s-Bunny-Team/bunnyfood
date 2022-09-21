from fastapi import Depends

from api import schemas
from api.crud.preferences import PreferencesCRUD
from api.dependencies import get_user, get_prefs_crud
from api.routers import APIRouter
from db import models

router = APIRouter()


@router.get(
    '/preferences/',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
def get_user_prefs(
        user: models.User = Depends(get_user),
        prefs: PreferencesCRUD = Depends(get_prefs_crud),
):
    """
    Get the user saved preferences.
    """
    return prefs.get_from_user(user)


@router.put(
    '/preferences/',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
def update_user_prefs(
        updated_prefs: schemas.UserPreferences,
        user: models.User = Depends(get_user),
        prefs: PreferencesCRUD = Depends(get_prefs_crud),
):
    """
    Update the user preferences.
    """
    return prefs.update(updated_prefs, user)
