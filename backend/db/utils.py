from . import db
from .secret import get_db_secret
from .models import SocialProfile, PostScore, Post, Location, UserPreferences, User


def init_db(
    user: str,
    password: str,
    host: str,
    database: str,
):
    db.init(
        user=user,
        password=password,
        host=host,
        database=database,
    )
    db.connect()
    # create_all_tables()


def init_db_from_secrets():
    init_db(
        user=get_db_secret()['username'],
        password=get_db_secret()['password'],
        host=get_db_secret()['host'],
        database=get_db_secret()['database'],
    )


def create_all_tables():
    db.create_tables(
        models=[SocialProfile, Location, Post, PostScore, UserPreferences, User]
    )
