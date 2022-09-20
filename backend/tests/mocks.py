import json
from abc import ABC
from pathlib import Path


class ClientMock(ABC):
    @staticmethod
    def load_json_fixture(path: str) -> dict:
        path = 'fixtures' / Path(path)
        with open(path, 'r') as f:
            return json.load(f)


class SFNMock(ClientMock):
    def __init__(self):
        self.started = False

    def start_execution(self, *args, **kwargs):
        self.started = True


class RekoMock(ClientMock):
    def __init__(
        self,
        detect_faces_resp: str = 'detect_faces.json',
        detect_labels_resp: str = 'detect_labels.json',
    ):
        self.detect_faces_resp = detect_faces_resp
        self.detect_labels_resp = detect_labels_resp

    def detect_faces(self, *args, **kwargs):
        return self.load_json_fixture(self.detect_faces_resp)

    def detect_labels(self, *args, **kwargs):
        return self.load_json_fixture(self.detect_labels_resp)
