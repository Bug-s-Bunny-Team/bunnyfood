from .models import ScrapingEvent
from .utils import create_service, create_scraper


def lambda_handler(event, context):
    event = ScrapingEvent(**event)

    print(event.json())

    scraper = create_scraper(event.scraper)
    print(f'using {scraper.__class__.__name__}')
    service = create_service(scraper)

    return service.process_event(event)
