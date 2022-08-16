import json
import os

from db.utils import init_db
from .sorting_service import BasicScoringService

def lambda_handler(event, context):
    try:
        init_db()
        sorterEvent = ListaDatiPost
        sorterEvent.sort(event)
        return 'Success'
    except Exception as e:
        print('Error processing Event {}'.format(json.dumps(event, indent=2)))
        raise e