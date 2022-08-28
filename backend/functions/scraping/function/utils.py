import os
import random

from db import get_session
from .download import Downloader
from .models import ScraperType
from .providers import AWSLocationProvider
from .scrapers import GramhirScraper, BaseScraper, PicukiScraper
from .service import ScrapingService

_session = get_session()


def create_gramhir_scraper() -> GramhirScraper:
    location_provider = AWSLocationProvider()
    scraper = GramhirScraper(location_provider=location_provider, session=_session)
    return scraper


def create_picuki_scraper() -> GramhirScraper:
    location_provider = AWSLocationProvider()
    scraper = PicukiScraper(location_provider=location_provider)
    return scraper


def create_scraper(type: ScraperType) -> BaseScraper:
    if type == ScraperType.RANDOM:
        types = list(ScraperType)
        types.remove(ScraperType.RANDOM)
        return create_scraper(random.choice(types))
    elif type == ScraperType.GRAMHIR:
        return create_gramhir_scraper()
    elif type == ScraperType.PICUKI:
        return create_picuki_scraper()


def create_service(scraper: BaseScraper) -> ScrapingService:
    downloader = Downloader(bucket_name=os.environ['BUCKET_NAME'])

    # set_random_proxy()

    service = ScrapingService(scraper=scraper, downloader=downloader, session=_session)

    return service
