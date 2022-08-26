from typing import Optional

import boto3
from sqlalchemy.orm import Session

from common.service import BaseService
from common.utils import s3_delete_file
from db import models
from .models import SortingPost, SortEvent


class SorterService(BaseService):
    def __init__(self, session: Session, bucket_name: str, aws_region='eu-central-1'):
        self._session = session
        self._bucket_name = bucket_name
        self._rekognition = boto3.client(
            service_name='rekognition', region_name=aws_region
        )

    def detect_person(self, name_image: str):
        # Analyze an image with Rekognition and return a bool if there is a person
        # name_image: name of the image to analyze
        # bucket: name of S3 bucket
        print("\n-------------------")
        print('detect_person')

        response = self._rekognition.detect_labels(
            Image={'S3Object': {'Bucket': self._bucket_name, 'Name': name_image}},
            MaxLabels=10,
        )
        print('Detecting person for ' + name_image)

        contain_person = False

        for label in response['Labels']:
            if label['Confidence'] >= 90:
                if label['Name'] == 'Person':
                    contain_person = True

        return contain_person

    def detect_sentiment_person(self, name_image: str):
        # Detect sentiment of a person with Rekognition and return a Dict of emotions and a bool if emotions were found
        # name_image: name of the image to analyze with Rekognition
        # bucket: name of S3 bucket
        print("\n-------------------")
        print('detect_sentiment_person')

        print(name_image)

        response = self._rekognition.detect_faces(
            Image={'S3Object': {'Bucket': self._bucket_name, 'Name': name_image}},
            Attributes=['ALL'],
        )
        contain_emotion = False
        emotions_dict = {}
        emotions_confid = []

        for faceDetail in response['FaceDetails']:
            emotions = faceDetail['Emotions']
            confid_single_face = {}
            for emotion in emotions:
                emotion_name = emotion['Type']
                emotion_confid_value = emotion['Confidence']
                if emotion_name != 'UNKNOWN':
                    confid_single_face[emotion_name] = emotion_confid_value

                    if emotion_confid_value >= 90:
                        if emotion_name in emotions_dict:
                            emotions_dict[emotion_name] += 1
                        else:
                            emotions_dict[emotion_name] = 1
                        contain_emotion = True
            emotions_confid.append(confid_single_face)
        return emotions_dict, contain_emotion, emotions_confid

    def analyze_image(self, name_image: str):
        # Analyze an image with Rekognition and return a Dict of emotions
        # name_image: name of the image to analyze
        print("\n-------------------")
        print("image_analyzer")

        emotions = {}
        emotions_confidence = {}

        print("\n-------------------")
        print(name_image)

        contain_person = self.detect_person(name_image)
        if contain_person:
            print("There is a person")

            (
                emotions,
                contain_emotion,
                emotions_confidence,
            ) = self.detect_sentiment_person(name_image)
            if contain_emotion:
                print("Emotion detected")
            else:
                print("No emotion detected")
        else:
            print("There is no person")

        print("-------------------\n")
        return emotions, emotions_confidence

    def calculate_image_score(self, post: SortingPost):
        if post.list_images:
            for image in post.list_images:
                image_name = image.name
                print("image name " + image_name)
                emotions, emotions_confidence = self.analyze_image(image_name)

                image.set_emotions(emotions)
                image.set_emotions_confidence(emotions_confidence)
        else:
            print("\n-------------------")
            print('no image in post')

        post.calculate_and_set_image_score()

    def _delete_post(self, post: SortingPost):
        for img in post.list_images:
            s3_delete_file(self._bucket_name, img.name)
        self._session.delete(
            self._session.query(models.Post).filter_by(id=post.id).first()
        )
        self._session.commit()

    def sort(self, post: SortingPost) -> Optional[SortingPost]:
        # Analyze a post with Rekognition for save or delete it
        # post: Post to analyze
        print("\n-------------------")
        print('sorting')

        # get image score with Rekognition
        self.calculate_image_score(post)

        if post.imageScore is not None:
            print("\n-------------------")
            print('save post')
            return post
        else:
            print("\n-------------------")
            print('delete post')
            self._delete_post(post)
            return None

    def process_event(self, event: SortEvent) -> dict:
        valid_posts = []
        for p in event.posts:
            db_post = self._session.query(models.Post).filter_by(id=p['id']).first()
            sorting_post = SortingPost.fromPost(db_post)
            sorting_post = self.sort(sorting_post)
            if sorting_post:
                valid_posts.append({'id': sorting_post.id})

        return {'posts_count': len(valid_posts), 'posts': valid_posts}
