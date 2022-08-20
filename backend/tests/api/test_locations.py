# from db import models, db
# from db.local_utils import create_all_tables, init_db
#
#
# def test_get_all_locations(api_client):
#     locations_models = [
#         models.Location(
#             name='test1', description='some desc', lat=43.5, long=54.3, score=4.5
#         ),
#         models.Location(
#             name='test2', description='some desc', lat=43.5, long=54.3, score=4.5
#         ),
#         models.Location(
#             name='test3', description='some desc', lat=43.5, long=54.3, score=4.5
#         ),
#     ]
#     models.Location.bulk_create(locations_models)
#
#     # locations = api_client.get('/locations')
#     # print(locations.json())
#     #
#     # assert locations.status_code == 200
#     # assert len(locations.json()) > 0
#
#
# def test_get_location_by_id(api_client):
#     location = api_client.get('/locations/666')
#
#     assert location.status_code == 404

import unittest
import pytest


# @pytest.mark.usefixtures('api_client')
# class LocationsTestCase(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def test_get_location_by_id(self, transaction):
#         location = self.api_client.get('/locations/666')
#
#         assert location.status_code == 404
from db import db
from db.utils import create_all_tables


def test_get_location_by_id(api_client, transaction):
        location = api_client.get('/locations/666')

        assert location.status_code == 404
