from typing import Optional

from instagram_private_api import Client as PrivateApi


class LocationProvider:
    def __init__(self, private_api: PrivateApi):
        self._private_api = private_api

    def search_location(self, query: str) -> Optional[dict]:
        rank_token = self._private_api.generate_uuid()
        results = self._private_api.location_fb_search(query, rank_token)
        if results['status'] == 'ok' and len(results) > 0:
            return results['items'][0]
        return None
