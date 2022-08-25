from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from api.auth import auth
from api.auth.jwt import JWTAuthorizationCredentials
from api.crud.locations import LocationsCRUD
from api.crud.profiles import ProfilesCRUD
from api.crud.preferences import PreferencesCRUD
from db import models, get_session


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def get_username(
    credentials: JWTAuthorizationCredentials = Depends(auth),
) -> str:
    try:
        return credentials.claims['cognito:username']
    except KeyError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Username missing')


def get_user(username: str = Depends(get_username), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
    return user


def get_prefs_crud(db: Session = Depends(get_db)) -> PreferencesCRUD:
    return PreferencesCRUD(db)


def get_locations_crud(db: Session = Depends(get_db)) -> LocationsCRUD:
    return LocationsCRUD(db)


def get_profiles_crud(db: Session = Depends(get_db)) -> ProfilesCRUD:
    return ProfilesCRUD(db)
