from .models import ScrapingEvent
from .utils import create_service, create_scraper


def lambda_handler(event, context):
    event = ScrapingEvent(**event)

    scraper = create_scraper(event.scraper)
    service = create_service(scraper)

    return service.process_event(event)
