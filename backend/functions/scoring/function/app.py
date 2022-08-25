from db import get_session

from .models import ScoringEvent
from .scoring_service import BasicScoringService


def lambda_handler(event, context):
    event = ScoringEvent(**event)

    session = get_session()
    service = BasicScoringService(session)

    return service.process_event(event)
