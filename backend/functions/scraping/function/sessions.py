import codecs
import json
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


class DDBSessionProvider(SessionProvider):
    def __init__(self, table_name: str, data_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dynamodb = boto3.resource('dynamodb')
        self._table = self._dynamodb.Table(table_name)
        self._data_key = data_key

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
        return item.get(self._data_key)

    def refresh_session(self, username: str, session_data: dict):
        self._table.update_item(
            Key={'username': username},
            UpdateExpression=f'SET {self._data_key} = :s',
            ExpressionAttributeValues={':s': session_data},
        )


class InstaloaderSessionProvider(DDBSessionProvider):
    def __init__(self, table_name: str):
        super().__init__(table_name, 'session_data')


class PrivateApiSessionProvider(DDBSessionProvider):
    def __init__(self, table_name: str):
        super().__init__(table_name, 'private_api_session_data')

    @staticmethod
    def _settings_to_json(python_object):
        if isinstance(python_object, bytes):
            return {
                '__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode(),
            }
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    @staticmethod
    def _settings_from_json(json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def get_session(self, username: str) -> Optional[dict]:
        session = super().get_session(username)
        if not session:
            return None
        session = json.loads(session, object_hook=self._settings_from_json)
        return session

    def refresh_settings(self, username: str, settings):
        self._table.update_item(
            Key={'username': username},
            UpdateExpression=f'SET {self._data_key} = :s',
            ExpressionAttributeValues={':s': json.dumps(settings, default=self._settings_to_json)},
        )

    def refresh_session(self, username: str, session_data: dict):
        raise NotImplementedError()
