import os
from typing import Optional
from .secret import get_db_secret

from . import db
from db.models import SocialProfile, PostScore, Post, Location


def init_db(
    user: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    database: Optional[str] = None,
):
    get_secret = True
    db.init(
        user=get_db_secret()["username"] if get_secret else os.environ['DB_USER'],
        password=get_db_secret()["password"] if get_secret else os.environ['DB_PASSWORD'],
        host=get_db_secret()["host"] if get_secret else os.environ['DB_HOST'],
        database=get_db_secret()["database"] if get_secret else os.environ['DB_NAME'],
    )
    db.connect()
    create_all_tables()


def create_all_tables():
    db.create_tables(models=[SocialProfile, Location, Post, PostScore])
