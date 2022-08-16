import boto3
from abc import ABC, abstractmethod
from db.utils import *
from db.models import *
from .models import ScoringPost

init_db()
create_all_tables()

class OutputStrategy(ABC):
    @abstractmethod
    def output(self, sPost: ScoringPost):
        pass

class S3OutputStrategy:
    outputBucket = os.environ['ENV_BUCKET_NAME']
    s3 = boto3.resource('s3')

    def output(self, sPost: ScoringPost):
        print(f'Writing output to {self.outputBucket} S3 Bucket')
        outputObject = self.s3.Object(self.outputBucket, f'scoring/{sPost.id}.json')
        outputObject.put(Body=sPost.toString())
        print(f'Successfully written output to {self.outputBucket} S3 Bucket')

class DBOutputStrategy:
    def output(self, sPost: ScoringPost):
        print(f'Writing output to Database')
        postScore = PostScore.get_or_create(post=sPost.id)[0]
        postScore.caption_score = sPost.captionScore
        postScore.media_score = sum(sPost.textsScore.values())/len(sPost.textsScore) if len(sPost.textsScore) != 0 else 0.0
        postScore.save()
        print(f'Successfully written output to Database')
