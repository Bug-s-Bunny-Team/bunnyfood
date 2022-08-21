from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.auth.jwt_auth import get_username
from db import SessionLocal, models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(username: str = Depends(get_username), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
