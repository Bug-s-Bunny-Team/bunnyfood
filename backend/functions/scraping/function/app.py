import json

from pydantic import ValidationError

from common.exceptions import ItemNotFoundException
from common.utils import create_error_response

from .models import ScrapingEvent
from .utils import create_service


def lambda_handler(event, context):
    try:
        # this is ugly, but for now it does the job
        event = ScrapingEvent(**json.loads(event['Records'][0]['Sns']['Message']))
    except ValidationError as e:
        return create_error_response(str(e))

    try:
        service = create_service()
    except ItemNotFoundException as e:
        return create_error_response(str(e), 500)

    return service.process_event(event)
