from functions.scoring.function.event_adapter import SNSEventAdapter
from functions.scoring.function.output_strategy import DBOutputStrategy
from functions.scoring.function.scoring_service import BasicScoringService

service = BasicScoringService(SNSEventAdapter(), DBOutputStrategy())
