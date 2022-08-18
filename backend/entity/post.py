import json
from typing import Dict, List

from common.utils import key_present_in_dict
from entity.image import Image
from entity.sentiment_comprehend import SentimentComprehend


class Post:
    id: int
    caption: str
    image_key: str
    list_images: List[Image]
    texts: Dict[int, str]
    hashtags: Dict[int, str]
    captionScore: SentimentComprehend
    imageScore: float
    textsScore: Dict[int, float]
    finalScore: float

    def __init__(self, id: str, caption: str, image_key: str, hashtags: Dict[int, str]):
        self.id = id
        self.caption = caption
        self.image_key = image_key
        self.image = None
        self.texts = dict()
        self.hashtags = hashtags
        self.captionScore = None
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

    def calculate_final_score(self):
        if self.captionScore:
            self.finalScore = self.captionScore.calculate_score()

    def set_caption_score(self, score: SentimentComprehend):
        self.captionScore = score

    def calculate_and_set_image_score(self):
        if self.list_images:
            count = 0
            for image in self.list_images:
                score = image.calculate_score()
                if score is not None:
                    count += 1
                    self.imageScore = (self.imageScore + score) if self.imageScore is not None else score
            if self.imageScore:
                self.imageScore = self.imageScore / count

    @classmethod
    def fromPost(cls, p):
        return cls(
            id=p.id,
            caption=p.caption,
            image_key=p.media_s3_key,
            hashtags={idx: string for idx, string in enumerate(p.hashtags)},
        )

    @classmethod
    def fromString(cls, string):
        in_json = json.loads(string)
        assert Post.__validate_input_json(in_json)
        return cls(
            id=in_json["id"],
            caption=in_json["caption"],
            image_key=in_json["image"],
            hashtags=in_json["hashtags"],
        )

    def toString(self):
        return json.dumps(self.__dict__)