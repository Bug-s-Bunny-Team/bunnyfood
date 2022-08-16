import json
from enum import Enum, unique
from typing import Dict
from common.utils import key_present_in_dict

@unique
class Score(str, Enum):
    MIXED = "MIXED"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"


class ScoringPost:
    id: int
    caption: str
    image: str
    texts: Dict[int, str]
    hashtags: Dict[int, str]
    captionScore: float
    textsScore: Dict[int, float]
    finalScore: float

    def __init__(self, id: str, caption: str, image: str, hashtags: Dict[int, str]):
        self.id = id
        self.caption = caption
        self.image = image
        self.texts = dict()
        self.hashtags = hashtags
        self.captionScore = 0.0
        self.textsScore = dict()
        self.finalScore = 0.0

    @classmethod
    def __validate_input_json(cls, in_json):
        return (
            key_present_in_dict(in_json, "id")
            & key_present_in_dict(in_json, "caption")
            & key_present_in_dict(in_json, "image")
            & key_present_in_dict(in_json, "hashtags")
        )

    @classmethod
    def fromPost(cls, p):
        return cls(
            id=p.id,
            caption=p.caption,
            image=p.media_s3_key,
            hashtags={idx: string for idx, string in enumerate(p.hashtags)},
        )

    @classmethod
    def fromString(cls, string):
        in_json = json.loads(string)
        assert ScoringPost.__validate_input_json(in_json)
        return cls(
            id=in_json["id"],
            caption=in_json["caption"],
            image=in_json["image"],
            hashtags=in_json["hashtags"],
        )

    def toString(self):
        return json.dumps(self.__dict__)
