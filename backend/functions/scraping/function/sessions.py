from abc import ABC, abstractmethod
from typing import Optional

import boto3

from common.exceptions import ItemNotFoundException


class SessionProvider(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_password(self, username: str) -> str:
        pass

    @abstractmethod
    def get_session(self, username: str) -> Optional[dict]:
        pass

    @abstractmethod
    def refresh_session(self, username: str, session_data: dict):
        pass


class InstagramSessionProvider(SessionProvider):
    def __init__(self, table_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dynamodb = boto3.resource('dynamodb')
        self._table = self._dynamodb.Table(table_name)

    def _get_table_item(self, username: str) -> dict:
        item = self._table.get_item(Key={'username': username}).get('Item')
        if not item:
            raise ItemNotFoundException(f'Table item not found for "{username}"')
        return item

    def get_password(self, username: str) -> str:
        item = self._get_table_item(username)
        return item.get('password')

    def get_session(self, username: str) -> Optional[dict]:
        item = self._get_table_item(username)
        return item.get('session_data')

    def refresh_session(self, username: str, session_data: dict):
        self._table.update_item(
            Key={'username': username},
            UpdateExpression='SET session_data = :s',
            ExpressionAttributeValues={':s': session_data}
        )
