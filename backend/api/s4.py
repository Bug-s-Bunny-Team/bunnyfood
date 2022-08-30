import datetime
import json
import os
import uuid
from abc import ABC, abstractmethod

import boto3

from api import ENV

__all__ = ['s4']


class BaseS4(ABC):
    """
    S4: Scraping Sorting Scoring Services
    """

    @abstractmethod
    def start(self, username: str):
        pass


class S4Dev(BaseS4):
    def __init__(self):
        self.runs = []

    def start(self, username: str):
        print(f'starting s4 for "{username}"')
        self.runs.append({'datetime': datetime.datetime.now(), 'username': username})


class S4(BaseS4):
    def __init__(self, s4_arn: str):
        self._client = boto3.client('stepfunctions')
        self._s4_arn = s4_arn

    def start(self, username: str):
        payload = {'username': username, 'posts_limit': 10}
        name = f'api-{username}-{uuid.uuid4()}'
        self._client.start_execution(
            stateMachineArn=self._s4_arn, input=json.dumps(payload), name=name
        )


def _create_s4():
    if ENV == 'prod':
        return S4(os.environ['S4_ARN'])
    return S4Dev()


s4 = _create_s4()
