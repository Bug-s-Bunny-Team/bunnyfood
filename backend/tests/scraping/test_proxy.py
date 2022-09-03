import pytest

from functions.scraping.function.proxy import get_random_proxy


@pytest.mark.vcr
def test_get_random_proxy():
    proxy = get_random_proxy()
    assert proxy
