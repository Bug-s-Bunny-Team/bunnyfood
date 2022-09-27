import pytest

from functions.sorter.function.sorting_service import SorterService
from tests.mocks import RekoMock


@pytest.fixture
def service(session) -> SorterService:
    service = SorterService(session, 'dummy-bucket')
    service._rekognition = RekoMock()
    return service
