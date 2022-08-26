import json
from abc import ABC, abstractmethod
from .models import ScoringPost

from db import SessionLocal, models

class EventAdapter(ABC):
    @abstractmethod
    def processEvent(self, event) -> ScoringPost:
        pass

class SQSEventAdapter(EventAdapter):
    def processEvent(self, event) -> ScoringPost:
        print("Processing SQS Event")
        post = ScoringPost.fromString(event['Records'][0]['body'])
        print("Successfully processed data")
        return post

class SNSEventAdapter(EventAdapter):
    def processEvent(self, event) -> ScoringPost:
        print("Processing SNS Event")
        post_id = json.loads(event['Records'][0]['Sns']['Message'])['post_id']
        with SessionLocal() as db:
            post = db.query(models.Post).filter_by(id=post_id).first()
        if not post:
            raise Exception(f'Post with id: {post_id}, not found in Database') 
        sPost = ScoringPost.fromPost(post)
        # print("Successfully processed data from SNS subject: " + event['Records'][0]['Sns']['Subject'])
        print("Successfully processed SNS message")
        return sPost
