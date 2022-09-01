from abc import ABC, abstractmethod
from typing import Optional

import boto3
import googlemaps

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


class MapsLocationProvider(BaseLocationProvider):
    def __init__(self, maps_api_key: str):
        self._maps = googlemaps.Client(key=maps_api_key)

    def search_location(self, query: str) -> Optional[LocationData]:
        geocode_result = self._maps.geocode(query)

        if not geocode_result:
            return None

        geocode_result = geocode_result[0]
        coords = geocode_result['geometry']['location']
        maps_place_id = geocode_result.get('place_id')

        place = self._maps.place(place_id=maps_place_id)
        address = place['result']['formatted_address']
        name = place['result']['name']
        types = place['result']['types']

        return LocationData(
            lat=coords['lat'],
            long=coords['lng'],
            address=address,
            maps_name=name,
            maps_place_id=maps_place_id,
            types=types
        )
