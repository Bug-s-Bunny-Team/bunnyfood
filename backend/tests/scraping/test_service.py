from functions.scraping.function.models import ScrapingEvent


def test_service(service):
    response = service.process_event(ScrapingEvent(username='antoniorazzi'))
    assert response['statusCode'] == 200
