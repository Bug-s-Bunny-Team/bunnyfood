from db import configure_session, SessionLocal
from .models import ScoringEvent
from .scoring_service import BasicScoringService


def lambda_handler(event, context):
    event = ScoringEvent(**event)

    configure_session()
    session = SessionLocal()
    service = BasicScoringService(session)

    return service.process_event(event)
