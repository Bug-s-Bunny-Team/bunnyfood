import pytest

from functions.scraping.function.scrapers import GramhirScraper


@pytest.fixture
def scraper():
    return GramhirScraper()


def test_search_user(scraper):
    gramhir_id = scraper._search_user('antoniorazzi')

    assert gramhir_id == '1571244992'


def test_get_profile_url(scraper):
    url = scraper._get_profile_url('antoniorazzi')

    assert url == 'https://gramhir.com/profile/antoniorazzi/1571244992'


def test_get_shortcode(scraper):
    shortcode = scraper._get_shortcode('https://gramhir.com/media/2913462245164671985')

    assert shortcode == 'ChusnnNjWPx'


def test_get_last_post(scraper):
    post = scraper.get_last_post('antoniorazzi')

    assert post
