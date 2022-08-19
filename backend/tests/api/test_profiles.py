# from api.schemas import SocialProfile
# from db import models
#
#
# def test_get_all_profiles(api_client, transaction):
#     a = models.SocialProfile(username='testuser').save()
#     profiles = api_client.get('/profiles')
#
#     assert profiles.status_code == 200
#     assert len(profiles.json()) > 0
#
#
# def test_get_profile_by_id(api_client):
#     profile = api_client.get('/profiles/666')
#
#     assert profile.status_code == 200
#     assert profile.json()['id'] == 666
#

# def test_add_profile(api_client, transaction):
#     profile = SocialProfile(username='testuser123')
#
#     res = api_client.post('/profiles/', data=profile.json())
#     created = models.SocialProfile.get_or_none(username='testuser123')
#
#     assert res.status_code == 201
#     assert created
