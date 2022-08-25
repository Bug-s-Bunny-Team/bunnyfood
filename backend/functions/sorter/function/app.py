from db import configure_session, SessionLocal

from .sorting_service import SorterService
from .models import SortEvent


def lambda_handler(event, context):
    event = SortEvent(**event)

    configure_session()
    session = SessionLocal()
    service = SorterService(session)

    return service.process_event(event)
