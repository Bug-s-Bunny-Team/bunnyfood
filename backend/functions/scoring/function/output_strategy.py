import os

import boto3
from abc import ABC, abstractmethod
from .models import ScoringPost

from db import SessionLocal, models, utils


class OutputStrategy(ABC):
    @abstractmethod
    def output(self, sPost: ScoringPost):
        pass


class S3OutputStrategy(OutputStrategy):
    outputBucket = os.environ['BUCKET_NAME']
    s3 = boto3.resource('s3')

    def output(self, sPost: ScoringPost):
        print(f'Writing output to {self.outputBucket} S3 Bucket')
        outputObject = self.s3.Object(self.outputBucket, f'scoring/{sPost.id}.json')
        outputObject.put(Body=sPost.toString())
        print(f'Successfully written output to {self.outputBucket} S3 Bucket')


class DBOutputStrategy(OutputStrategy):
    def output(self, sPost: ScoringPost):
        print(f'Writing output to Database')
        # TODO: write the final score to the location
        # postScore = PostScore.get_or_create(post=sPost.id)[0]
        # postScore.caption_score = sPost.captionScore
        # postScore.media_score = sum(sPost.textsScore.values())/len(sPost.textsScore) if len(sPost.textsScore) != 0 else 0.0
        # postScore.save()
        print(f'Successfully written output to Database')
