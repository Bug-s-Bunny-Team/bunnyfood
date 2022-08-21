from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_user
from api import schemas

from db.utils import get_or_create
from db import models

router = APIRouter()


@router.get(
    '/preferences/',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
def get_user_prefs(
    user: models.User = Depends(get_user), db: Session = Depends(get_db)
):
    prefs = get_or_create(db, models.UserPreferences, user=user)
    return prefs


@router.put(
    '/preferences/',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
def update_user_prefs(
    updated_prefs: schemas.UserPreferences,
    user: models.User = Depends(get_user),
    db: Session = Depends(get_db),
):
    prefs = get_or_create(db, models.UserPreferences, user=user)
    prefs.default_guide_view = updated_prefs.default_guide_view
    db.add(prefs)
    db.commit()
    return prefs
