import json
from enum import Enum
from typing import List, Dict

from common.models import LambdaEvent
from common.utils import key_present_in_dict


class SortEvent(LambdaEvent):
    posts_count: int
    posts: list


class Emotions(float, Enum):
    HAPPY = 1
    SURPRISED = 0.6
    CALM = 0.4
    SAD = 0.2
    CONFUSED = 0.15
    ANGRY = 0.1
    DISGUSTED = 0
    FEAR = 0


class Image:
    name: str
    emotions: {}
    emotions_confidence: []

    def __init__(self, name: str):
        self.name = name
        self.emotions = {}
        self.emotions_confidence = []

    def set_emotions(self, emotions: dict):
        self.emotions = emotions

    def set_emotions_confidence(self, emotions_confid: List[dict]):
        self.emotions_confidence = emotions_confid

    def get_emotions_confidence(self) -> List[dict]:
        return self.emotions_confidence

    def calculate_score(self):
        if self.emotions:
            value_sum = 0.0
            sum_weights = 0.0
            for emotion, num in self.emotions.items():
                value_sum += Emotions[emotion].value * num
                sum_weights += num
            return 100 * value_sum / sum_weights
        else:
            return None

    # to string
    def __str__(self) -> str:
        return "image name: " + str(self.name)


class SortingPost:
    id: int
    caption: str
    list_images: List[Image]
    texts: Dict[int, str]
    hashtags: Dict[int, str]
    imageScore: float
    textsScore: Dict[int, float]
    finalScore: float

    def __init__(self, id: str, caption: str, list_images: List[Image]):
        self.id = id
        self.caption = caption
        self.list_images = list_images
        self.texts = dict()
        self.hashtags = dict()
        self.imageScore = 0.0
        self.textsScore = dict()
        self.finalScore = 0.0

    def __validate_input_json(self, in_json):
        return (
                key_present_in_dict(in_json, "id")
                & key_present_in_dict(in_json, "caption")
                & key_present_in_dict(in_json, "image")
                & key_present_in_dict(in_json, "hashtags")
        )

    def calculate_and_set_image_score(self):
        if self.list_images:
            count = 0
            for image in self.list_images:
                score = image.calculate_score()
                if score is not None:
                    count += 1
                    self.imageScore = (
                        (self.imageScore + score)
                        if self.imageScore is not None
                        else score
                    )
            if self.imageScore:
                self.imageScore = self.imageScore / count

    @classmethod
    def fromPost(cls, p):
        return cls(
            id=p.id,
            caption=p.caption,
            list_images=[Image(p.media_s3_key)]
        )

    def toString(self):
        return json.dumps(self.__dict__)
