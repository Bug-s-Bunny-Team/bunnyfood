from pydantic import Extra
from sqlalchemy.orm import Session

from common.models import LambdaEvent
from common.service import BaseService
from db import models


class SignupEvent(LambdaEvent):
    userName: str

    class Config:
        extra = Extra.allow


class SignupService(BaseService):
    def __init__(self, session: Session):
        self._session = session

    def process_event(self, event: SignupEvent) -> dict:
        print(f'checking if "{event.userName}" is already in db')
        user = self._session.query(models.User).filter_by(username=event.userName).first()
        if not user:
            print('user not in db, creating')
            user = models.User(username=event.userName)
            self._session.add(user)
            self._session.commit()
            return {'created': True}
        else:
            print('user already in db')
            return {'created': False}
