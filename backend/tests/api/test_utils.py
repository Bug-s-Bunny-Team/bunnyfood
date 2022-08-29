from api.utils import search_social_profile


def test_search_profile_existing():
    exists = search_social_profile('antoniorazzi')

    assert exists


def test_search_profile_not_existing():
    exists = search_social_profile('thisdoesnotexistsblaudbsui384')

    assert not exists
