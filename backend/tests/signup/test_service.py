from functions.signup.function.service import SignupService, SignupEvent


def test_signup_new_user(session):
    event = SignupEvent(userName='somenewuser123')
    service = SignupService(session)

    result = service.process_event(event)

    assert result['created']


def test_signup_existing_user(session):
    event = SignupEvent(userName='testuser')
    service = SignupService(session)

    result = service.process_event(event)

    assert not result['created']
