from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.auth.jwt_auth import get_username
from api.dependencies import get_db
from api import schemas

from db.utils import get_or_create
from db import models

router = APIRouter()


@router.get(
    '/preferences/',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
def get_user_prefs(username: str = Depends(get_username), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    prefs = get_or_create(db, models.UserPreferences, user=user)
    return prefs
