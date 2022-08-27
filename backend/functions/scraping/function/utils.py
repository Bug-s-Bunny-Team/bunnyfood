import os

from instagram_private_api import Client as PrivateApi

from db import get_session
from .custom import CustomInstaloader
from .download import Downloader
from .providers import PrivateApiLocationProvider, AWSLocationProvider
from .proxy import set_random_proxy
from .scrapers import InstagramScraper, GramhirScraper
from .service import ScrapingService
from .sessions import InstaloaderSessionProvider, PrivateApiSessionProvider


def create_private_api() -> PrivateApi:
    insta_username = os.environ['INSTA_USERNAME']
    sessions_table = os.environ['INSTA_SESSIONS_TABLE']

    session_provider = PrivateApiSessionProvider(sessions_table)

    session = session_provider.get_session(insta_username)
    password = session_provider.get_password(insta_username)
    if session:
        print('using saved session')
        client = PrivateApi(insta_username, password, settings=session, auto_patch=True)
    else:
        print('session not found, logging in')
        client = PrivateApi(insta_username, password, auto_patch=True)
        session_provider.refresh_settings(insta_username, client.settings)

    return client


def create_instagram_scraper() -> InstagramScraper:
    insta_username = os.environ['INSTA_USERNAME']
    sessions_table = os.environ['INSTA_SESSIONS_TABLE']

    session_provider = InstaloaderSessionProvider(sessions_table)
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


def create_gramhir_scraper() -> GramhirScraper:
    location_provider = AWSLocationProvider()

    scraper = GramhirScraper(location_provider)

    return scraper


def create_service() -> ScrapingService:
    # scraper = create_instagram_scraper()
    scraper = create_gramhir_scraper()
    downloader = Downloader(bucket_name=os.environ['BUCKET_NAME'])
    session = get_session()
    # set_random_proxy()

    service = ScrapingService(scraper=scraper, downloader=downloader, session=session)

    return service
