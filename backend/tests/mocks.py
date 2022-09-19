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
