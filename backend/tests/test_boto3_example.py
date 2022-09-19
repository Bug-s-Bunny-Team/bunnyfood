import boto3
import pytest

from mocks import ClientMock


class ComprehendMock(ClientMock):
    def __init__(
        self, detect_dominant_language_resp: str = 'detect_dominant_it.json'
    ):
        self.detect_dominant_language_resp = detect_dominant_language_resp

    def detect_dominant_language(self, *args, **kwargs):
        return self.load_json_fixture(self.detect_dominant_language_resp)


class ClassToTest:
    """
    Just an example class, very similar to ScoringService or SortingService
    """

    def __init__(self):
        self._comprehend_client = boto3.client(service_name='comprehend')

    def something_using_comprehend(self) -> bool:
        resp = self._comprehend_client.detect_dominant_language(Text='some stuff')
        return resp['ResultList'][0]['Languages'][0]['LanguageCode'] == 'it'


@pytest.fixture(scope='session')
def instance_to_test() -> ClassToTest:
    instance = ClassToTest()
    instance._comprehend_client = ComprehendMock()
    return instance


def test_comprehend_response(instance_to_test):
    assert instance_to_test.something_using_comprehend()

    instance_to_test._comprehend_client.detect_dominant_language_resp = 'detect_dominant_en.json'
    assert not instance_to_test.something_using_comprehend()
