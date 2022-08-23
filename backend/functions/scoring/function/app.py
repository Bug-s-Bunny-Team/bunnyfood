from .models import ScoringEvent
from .scoring_service import BasicScoringService
from .event_adapter import SNSEventAdapter
from .output_strategy import DBOutputStrategy


def lambda_handler(event, context):
    event = ScoringEvent(**event)
    service = BasicScoringService(SNSEventAdapter(), DBOutputStrategy())
    return service.process_event(event)
