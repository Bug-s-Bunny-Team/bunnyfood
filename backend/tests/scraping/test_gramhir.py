import pytest

from db import models
from functions.scraping.function.scrapers import GramhirScraper


@pytest.fixture
def scraper(session):
    return GramhirScraper(session)


@pytest.mark.vcr
def test_search_user(scraper):
    gramhir_id = scraper._get_profile_internal_id('antoniorazzi')

    assert gramhir_id == '1571244992'

    session = scraper._session
    cache = session.query(models.GramhirProfiles).filter_by(username='antoniorazzi').first()
    assert cache.gramhir_id == '1571244992'


@pytest.mark.vcr
def test_get_profile_url(scraper):
    url = scraper._get_profile_url('antoniorazzi')

    assert url == 'https://gramhir.com/profile/antoniorazzi/1571244992'


@pytest.mark.vcr
def test_get_shortcode(scraper):
    shortcode = scraper._get_shortcode('https://gramhir.com/media/2913462245164671985')

    assert shortcode == 'ChusnnNjWPx'


@pytest.mark.vcr
def test_get_last_post(scraper):
    post = scraper.get_last_post('antoniorazzi')

    assert post


@pytest.mark.vcr
def test_get_last_posts(scraper):
    posts = scraper.get_last_posts('antoniorazzi', 5)

    assert len(posts) == 5
