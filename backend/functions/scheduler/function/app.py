import os

from db import get_session
from .service import SchedulerEvent, SchedulerService


def lambda_handler(event, context):
    event = SchedulerEvent(**event)
    session = get_session()

    service = SchedulerService(session, os.environ['S4_ARN'])
    return service.process_event(event)
