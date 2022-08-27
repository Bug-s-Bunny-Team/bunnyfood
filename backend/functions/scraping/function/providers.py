from abc import ABC, abstractmethod
from typing import Optional

import boto3
from instagram_private_api import Client as PrivateApi


class BaseLocationProvider(ABC):
    @abstractmethod
    def search_location(self, query: str) -> Optional[dict]:
        pass


class AWSLocationProvider(BaseLocationProvider):
    def __init__(self):
        self._client = boto3.client('location')

    def search_location(self, query: str) -> Optional[dict]:
        response = self._client.search_place_index_for_text(
            IndexName='explore.place', MaxResults=1, Text=query
        )
        results = response['Results']
        if len(results) == 0:
            return None
        coords = results[0]['Place']['Geometry']['Point']
        return {'long': coords[0], 'lat': coords[1]}


class PrivateApiLocationProvider(BaseLocationProvider):
    def __init__(self, private_api: PrivateApi):
        self._private_api = private_api

    def search_location(self, query: str) -> Optional[dict]:
        rank_token = self._private_api.generate_uuid()
        results = self._private_api.location_fb_search(query, rank_token)
        if results['status'] == 'ok' and len(results) > 0:
            return results['items'][0]
        return None
