from db import get_session
from .service import SignupEvent, SignupService


def lambda_handler(event, context):
    signup_event = SignupEvent(**event)
    session = get_session()

    service = SignupService(session)
    service.process_event(signup_event)

    return event
