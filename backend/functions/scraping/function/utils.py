import os

from db import get_session
from .download import Downloader
from .providers import AWSLocationProvider
from .scrapers import GramhirScraper
from .service import ScrapingService


def create_gramhir_scraper() -> GramhirScraper:
    location_provider = AWSLocationProvider()
    scraper = GramhirScraper(location_provider)
    return scraper


def create_service() -> ScrapingService:
    scraper = create_gramhir_scraper()
    downloader = Downloader(bucket_name=os.environ['BUCKET_NAME'])
    session = get_session()
    # set_random_proxy()

    service = ScrapingService(scraper=scraper, downloader=downloader, session=session)

    return service
