from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import schemas, models

# from api.auth.jwt_auth import get_current_user
from api.dependencies import get_db

router = APIRouter()


def get_or_create(db: Session, model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance


@router.get(
    # '/preferences',
    '/preferences/{username}',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
# def get_user_prefs(username: str = Depends(get_current_user)):
def get_user_prefs(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    prefs = get_or_create(db, models.UserPreferences, user=user)
    return prefs
