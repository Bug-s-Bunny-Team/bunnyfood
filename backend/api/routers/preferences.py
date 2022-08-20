from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import db.models
from api import schemas, models

# from api.auth.jwt_auth import get_current_user
from api.dependencies import get_db
from db.utils import get_or_create

router = APIRouter()


@router.get(
    # '/preferences',
    '/preferences/{username}',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
# def get_user_prefs(username: str = Depends(get_current_user)):
def get_user_prefs(username: str, db: Session = Depends(get_db)):
    user = db.query(db.models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    prefs = get_or_create(db, db.models.UserPreferences, user=user)
    return prefs
