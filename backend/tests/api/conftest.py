import pytest
from fastapi.testclient import TestClient

from db import db
from db.utils import create_all_tables, init_db
from api.main import app


@pytest.fixture
def transaction():
    init_db('user', 'password', 'localhost', 'bunnyfood_test')
    with db.transaction() as txn:
        create_all_tables()
        yield txn
        txn.rollback()


@pytest.fixture(scope='class')
def api_client(request):
    request.cls.api_client = TestClient(app)
