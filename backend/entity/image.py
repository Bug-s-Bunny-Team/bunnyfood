from enum import Enum
from typing import List


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

    # def toString(self):
    #  return json.dumps(self.__dict__)
