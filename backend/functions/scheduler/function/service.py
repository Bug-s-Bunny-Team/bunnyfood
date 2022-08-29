import datetime
import json
from typing import List, Optional

import boto3
from sqlalchemy.orm import Session

from common.models import LambdaEvent
from common.service import BaseService
from db import models


class SchedulerEvent(LambdaEvent):
    last_scrape_gte: int = 1
    limit: int = 15


class SchedulerService(BaseService):
    def __init__(self, session: Session, s4_arn: str):
        self._session = session
        self._s4_arn = s4_arn
        self._client = None

    def _start_s4(self, username: str):
        if not self._client:
            self._client = boto3.client('stepfunctions')
        payload = {'username': username, 'posts_limit': 10}
        self._client.start_execution(
            stateMachineArn=self._s4_arn, input=json.dumps(payload)
        )

    def _get_profiles(
        self, last_scrape_gte: int, limit: Optional[int] = None
    ) -> List[models.SocialProfile]:
        now = datetime.datetime.now()
        profiles = (
            self._session.query(models.SocialProfile)
            .filter(
                models.SocialProfile.last_scraped
                >= now + datetime.timedelta(hours=last_scrape_gte)
            )
            .order_by(models.SocialProfile.last_scraped.desc())
        )
        if limit:
            profiles = profiles.limit(limit)
        profiles = profiles.all()
        return profiles

    def process_event(self, event: SchedulerEvent) -> dict:
        profiles = self._get_profiles(event.last_scrape_gte, event.limit)
        profiles_count = len(profiles)

        print(f'scheduling {profiles_count} profiles to execution in s4')
        for p in profiles:
            self._start_s4(p.username)

        return {
            'profiles_count': profiles_count,
            'profiles': [{'id': p.id, 'username': p.username} for p in profiles],
        }
