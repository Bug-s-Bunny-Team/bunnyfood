import os

from db import db
from db.utils import init_db, create_all_tables


def db_connect():
    username = os.environ.get('DB_USER', 'user')
    password = os.environ.get('DB_PASS', 'password')
    host = os.environ.get('DB_HOST', 'localhost')
    database = os.environ.get('DB_NAME', 'bunnyfood_dev')

    init_db(
        user=username,
        password=password,
        host=host,
        database=database,
    )

    # create_all_tables()


def get_db():
    try:
        db_connect()
        yield
    finally:
        if not db.is_closed():
            db.close()
