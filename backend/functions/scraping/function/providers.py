from abc import ABC, abstractmethod
from typing import Optional

import boto3

from .models import LocationData


class BaseLocationProvider(ABC):
    @abstractmethod
    def search_location(self, query: str) -> Optional[LocationData]:
        pass


class AWSLocationProvider(BaseLocationProvider):
    def __init__(self):
        self._client = boto3.client('location')

    def search_location(self, query: str) -> Optional[LocationData]:
        response = self._client.search_place_index_for_text(
            IndexName='explore.place', MaxResults=1, Text=query
        )
        results = response['Results']

        if len(results) == 0:
            return None

        coords = results[0]['Place']['Geometry']['Point']
        return LocationData(long=coords[0], lat=coords[1])
