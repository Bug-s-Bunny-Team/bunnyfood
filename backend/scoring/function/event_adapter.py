import json
from abc import ABC, abstractmethod
from db.utils import *
from db.models import *
from .models import ScoringPost

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
        post = Post.get_or_none(id=post_id)
        if not post:
            raise Exception(f'Post with id: {post_id}, not found in Database') 
        sPost = ScoringPost.fromPost(post)
        # print("Successfully processed data from SNS subject: " + event['Records'][0]['Sns']['Subject'])
        print("Successfully processed SNS message")
        return sPost
