from abc import ABC
from typing import Type, Optional

from playhouse.shortcuts import model_to_dict

from common.models import Request
from common.utils import create_error_response, create_response
from db.models import BaseModel


class DataProvider(ABC):
    def __init__(self, model: Type[BaseModel]):
        self.model = model

    @staticmethod
    def serialize(result) -> dict:
        return model_to_dict(result)

    def query_by_id(self, entity_id: int) -> Optional:
        return self.model.get_or_none(id=entity_id)

    def query_all(self):
        return self.model.select()

    def get_by_id(self, entity_id: int) -> dict:
        result = self.query_by_id(entity_id)
        if not result:
            return create_error_response(f'{self.model.__name__} not found', 404)
        return create_response(self.serialize(result), 200)

    def get_all(self) -> dict:
        results = [self.serialize(r) for r in self.query_all()]
        return create_response(results, 200)

    def handle_request(self, request: Request):
        parts = request.path.removeprefix('/').split('/')
        if len(parts) > 1:
            entity_id = int(parts[1])
            return self.get_by_id(entity_id)
        return self.get_all()
