from abc import ABC

from sqlalchemy.orm import Session


class BaseCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db
