import os
from abc import ABC
from typing import Optional

import boto3

from entity.post import Post
from entity.sentiment_comprehend import SentimentComprehend


class SorterService(ABC):
    def __init__(self, aws_region='eu-central-1'):
        self._rekognition = boto3.client(service_name='rekognition', region_name=aws_region)
        self._comprehend = boto3.client(service_name='comprehend', region_name=aws_region)

    def __detect_language_text(self, text: str) -> str:
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
        print(language)
        return language

    def __detect_sentiment_text(self, post: Post, language) -> Optional[SentimentComprehend]:
        # Detect sentiment of a post with Comprehend and return score
        # post: post to analyze with Comprehend
        # param language: language of the caption
        print("\n-------------------")
        print('detect_sentiment_text')

        # Below we check all the languages supported by AWS Comprehend
        if language in ['ar', 'hi', 'ko', 'zh-TW', 'ja', 'zh', 'de', 'pt', 'en', 'it', 'fr', 'es']:
            # result of comprehend
            json_result = self._comprehend.detect_sentiment(Text=post.caption, LanguageCode=language)

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

    def __detect_labels(self, name_image: str, bucket: str):
        # Detect object of an image with Rekognition and return a Dict of labels and a bool if there is a person
        # name_image: name of the image to analyze
        # bucket: name of S3 bucket
        print("\n-------------------")
        print('detect_labels')

        response = self._rekognition.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': name_image}},
                                                   MaxLabels=10)
        print('Detecting labels for ' + name_image)

        labels_dict = {}
        contain_person = False

        for label in response['Labels']:
            if label['Confidence'] >= 90:
                if label['Name'] == 'Person':
                    contain_person = True
                else:
                    for parent in label['Parents']:
                        if parent['Name'] == 'Food':
                            if label['Name'] in labels_dict:
                                labels_dict[label['Name']] += 1
                            else:
                                labels_dict[label['Name']] = 1
        return labels_dict, contain_person

    def __detect_sentiment_person(self, name_image: str, bucket: str):
        # Detect sentiment of a person with Rekognition and return a Dict of emotions and a bool if emotions were found
        # name_image: name of the image to analyze with Rekognition
        # bucket: name of S3 bucket
        print("\n-------------------")
        print('detect_sentiment_person')

        print(name_image)

        response = self._rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': name_image}},
                                                  Attributes=['ALL'])
        contain_emotion = True
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
                        contain_emotion = False
            emotions_confid.append(confid_single_face)
        return emotions_dict, contain_emotion, emotions_confid

    def __analyze_image(self, name_image: str):
        # Analyze an image with Rekognition and return a Dict of labels and emotions
        # name_image: name of the image to analyze
        print("\n-------------------")
        print("image_analyzer")

        bucket = 'test-bucket-backend-bugsbunny'
        emotions = {}
        emotions_confidence = {}

        print("\n-------------------")
        print(name_image)

        labels, contain_person = self.__detect_labels(name_image, bucket)
        if contain_person:
            print("There is a person")

            emotions, contain_emotion, emotions_confidence = self.__detect_sentiment_person(name_image, bucket)
            if not contain_emotion:
                print("Emotion detected")
            else:
                print("No emotion detected")
        else:
            print("There is no person")

        print("-------------------\n")
        return labels, emotions, emotions_confidence

    def calculate_text_score(self, post: Post) -> float:
        if post.caption:
            score = self.__detect_sentiment_text(post, self.__detect_language_text(post.caption))
            post.set_caption_score(score)
            post.calculate_final_score()

        return post.finalScore

    def calculate_image_score(self, post: Post):
        if post.list_images:
            for image in post.list_images:
                image_name = image.name
                print("image name " + image_name)
                labels, emotions, emotions_confidence = self.__analyze_image(image_name)

                image.set_labels(labels)
                image.set_emotions(emotions)
                image.set_emotions_confidence(emotions_confidence)
        else:
            print("\n-------------------")
            print('no image in post')

        post.calculate_and_set_image_score()

    def sort(self, post: Post):
        # Analyze a post with Rekognition and Comprehend for save or delete it
        # post: Post to analyze
        print("\n-------------------")
        print('sorting')

        # calculate score caption with comprehend

        text_score = self.calculate_text_score(post)

        print("\ncomprehend score: " + str(text_score) if text_score else 'no text found' + "\n-------------------\n")

        # get image score with Rekognition
        self.calculate_image_score(post)
        image_score = post.imageScore

        if image_score is not None or text_score is not None:
            print("\n-------------------")
            print('save post')
        else:
            print("\n-------------------")
            print('delete post')
