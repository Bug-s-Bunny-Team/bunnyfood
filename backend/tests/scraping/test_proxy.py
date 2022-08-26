from functions.scraping.function.proxy import get_random_proxy


def test_get_random_proxy(monkeypatch):
    proxy = get_random_proxy()
    assert proxy
