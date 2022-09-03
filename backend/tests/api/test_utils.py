import pytest

from api.utils import search_social_profile


@pytest.mark.vcr
def test_search_profile_existing():
    exists = search_social_profile('antoniorazzi')

    assert exists


@pytest.mark.vcr
def test_search_profile_not_existing():
    exists = search_social_profile('thisdoesnotexistsblaudbsui384')

    assert not exists
