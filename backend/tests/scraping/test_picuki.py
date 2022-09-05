import pytest

from functions.scraping.function.scrapers import PicukiScraper


@pytest.fixture
def scraper():
    return PicukiScraper()


@pytest.mark.vcr
def test_get_profile_url(scraper):
    url = scraper._get_profile_url('antoniorazzi')

    assert url == 'https://picuki.com/profile/antoniorazzi'


@pytest.mark.vcr
def test_get_shortcode(scraper):
    shortcode = scraper._get_shortcode('https://picuki.com/media/2913462245164671985')

    assert shortcode == 'ChusnnNjWPx'


@pytest.mark.vcr
def test_get_last_post(scraper):
    post = scraper.get_last_post('antoniorazzi')

    assert post
