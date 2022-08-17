from pytest import fixture
from fastapi.testclient import TestClient

from backend.api.main import app


@fixture
def api_client() -> TestClient:
    return TestClient(app)
