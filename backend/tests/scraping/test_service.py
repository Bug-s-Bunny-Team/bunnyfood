from functions.scraping.function.models import ScrapingEvent


def test_service_last_post(service):
    response = service.process_event(
        ScrapingEvent(username='antoniorazzi', posts_limit=1)
    )

    assert response['posts_count'] == 1


def test_service_n_posts(service):
    response = service.process_event(
        ScrapingEvent(username='antoniorazzi', posts_limit=4)
    )

    assert response['posts_count'] == 4
