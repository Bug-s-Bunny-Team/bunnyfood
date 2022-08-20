import json
import os

from .scoring_service import BasicScoringService
from .event_adapter import SQSEventAdapter, SNSEventAdapter
from .output_strategy import S3OutputStrategy, DBOutputStrategy


def lambda_handler(event, context):
    try:
        scoringService = BasicScoringService(SNSEventAdapter(), DBOutputStrategy())
        scoringService.score(event)
        return 'Success'
    except Exception as e:
        print('Error processing Event {}'.format(json.dumps(event, indent=2)))
        raise e
