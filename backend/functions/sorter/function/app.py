import os

from db import get_session
from .models import SortEvent
from .sorting_service import SorterService


def lambda_handler(event, context):
    event = SortEvent(**event)

    session = get_session()
    service = SorterService(session, os.environ['BUCKET_NAME'])

    return service.process_event(event)
