import os

from .custom import CustomInstaloader
from .scrapers import InstagramScraper
from .sessions import InstagramSessionProvider


def create_scraper() -> InstagramScraper:
    insta_username = os.environ['INSTA_USERNAME']
    sessions_table = os.environ['INSTA_SESSIONS_TABLE']

    session_provider = InstagramSessionProvider(sessions_table)
    insta = CustomInstaloader()

    session = session_provider.get_session(insta_username)
    if session:
        print('using saved session')
        insta.import_session_from_dict(session, insta_username)
    else:
        print('session not found, logging in')
        insta_password = session_provider.get_password(insta_username)
        insta.login(insta_username, insta_password)
        session_provider.refresh_session(insta_username, insta.export_session_as_dict())

    return InstagramScraper(client=insta)
