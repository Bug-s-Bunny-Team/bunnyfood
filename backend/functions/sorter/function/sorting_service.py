import os
from typing import Optional

import boto3
from sqlalchemy.orm import Session

from common.service import BaseService
from db import models
from .models import SortingPost, SentimentComprehend, SortEvent


class SorterService(BaseService):
    def __init__(self, session: Session, aws_region='eu-central-1'):
        self._session = session
        self._rekognition = boto3.client(
            service_name='rekognition', region_name=aws_region
        )
        self._comprehend = boto3.client(
            service_name='comprehend', region_name=aws_region
        )

    def detect_language_text(self, text: str) -> str:
        # Detect language of a text with Comprehend and return (str).
        # text: text to analyze with Comprehend

        print("\n-------------------")
        print('detect_language_text')

        # result of comprehend
        json_result = self._comprehend.detect_dominant_language(Text=text)

        # get first language
        languages = json_result['Languages'][0]

        # get language code
        language = languages['LanguageCode']
        return language

    def detect_sentiment_text(
        self, post: SortingPost, language
    ) -> Optional[SentimentComprehend]:
        # Detect sentiment of a post with Comprehend and return score
        # post: post to analyze with Comprehend
        # param language: language of the caption
        print("\n-------------------")
        print('detect_sentiment_text')

        # Below we check all the languages supported by AWS Comprehend
        if language in [
            'ar',
            'hi',
            'ko',
            'zh-TW',
            'ja',
            'zh',
            'de',
            'pt',
            'en',
            'it',
            'fr',
            'es',
        ]:
            # result of comprehend
            json_result = self._comprehend.detect_sentiment(
                Text=post.caption, LanguageCode=language
            )

            # get sentiment
            array = json_result["SentimentScore"]
            principal_sentiment = json_result["Sentiment"]

            mult_factor = 100

            # get sentiment score
            negative = int(array["Negative"] * mult_factor)
            neutral = int(array["Neutral"] * mult_factor)
            positive = int(array["Positive"] * mult_factor)
            mixed = int(array["Mixed"] * mult_factor)

            score = SentimentComprehend(negative, positive, neutral, mixed)
            score.set_sentiment(principal_sentiment)

            return score
        else:
            return None

    def detect_person(self, name_image: str, bucket: str):
        # Analyze an image with Rekognition and return a bool if there is a person
        # name_image: name of the image to analyze
        # bucket: name of S3 bucket
        print("\n-------------------")
        print('detect_person')

        response = self._rekognition.detect_labels(
            Image={'S3Object': {'Bucket': os.environ[bucket], 'Name': name_image}},
            MaxLabels=10,
        )
        print('Detecting person for ' + name_image)

        contain_person = False

        for label in response['Labels']:
            if label['Confidence'] >= 90:
                if label['Name'] == 'Person':
                    contain_person = True

        return contain_person

    def detect_sentiment_person(self, name_image: str, bucket: str):
        # Detect sentiment of a person with Rekognition and return a Dict of emotions and a bool if emotions were found
        # name_image: name of the image to analyze with Rekognition
        # bucket: name of S3 bucket
        print("\n-------------------")
        print('detect_sentiment_person')

        print(name_image)

        response = self._rekognition.detect_faces(
            Image={'S3Object': {'Bucket': os.environ[bucket], 'Name': name_image}},
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

        bucket = 'test-bucket-backend-bugsbunny'
        emotions = {}
        emotions_confidence = {}

        print("\n-------------------")
        print(name_image)

        contain_person = self.detect_person(name_image, bucket)
        if contain_person:
            print("There is a person")

            (
                emotions,
                contain_emotion,
                emotions_confidence,
            ) = self.detect_sentiment_person(name_image, bucket)
            if contain_emotion:
                print("Emotion detected")
            else:
                print("No emotion detected")
        else:
            print("There is no person")

        print("-------------------\n")
        return emotions, emotions_confidence

    def calculate_text_score(self, post: SortingPost) -> float:
        if post.caption:
            score = self.detect_sentiment_text(
                post, self.detect_language_text(post.caption)
            )
            post.set_caption_score(score)
            post.calculate_final_score()

        return post.finalScore

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

    def sort(self, post: SortingPost) -> Optional[SortingPost]:
        # Analyze a post with Rekognition and Comprehend for save or delete it
        # post: Post to analyze
        print("\n-------------------")
        print('sorting')

        # calculate score caption with comprehend
        #
        # text_score = self.calculate_text_score(post)
        #
        # print(
        #     "\ncomprehend score: " + str(text_score)
        #     if text_score
        #     else 'no text found' + "\n-------------------\n"
        # )

        # get image score with Rekognition
        self.calculate_image_score(post)

        if post.imageScore is not None:
            print("\n-------------------")
            print('save post')
            return post
        else:
            print("\n-------------------")
            print('delete post')
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
