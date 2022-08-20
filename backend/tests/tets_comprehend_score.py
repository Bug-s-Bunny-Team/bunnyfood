import json
import boto3
from typing import Dict
from pathlib import Path
from enum import Enum, unique

@unique
class Score(str, Enum):
    MIXED = "MIXED"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"

class ScoringPost:
    id: int
    caption: str
    texts: Dict[int, str]
    captionScore: float
    textsScore: Dict[int, float]
    finalScore: float

    def __init__(self, id: str, caption: str):
        self.id = id
        self.caption = caption
        self.texts = dict()
        self.captionScore = 0.0
        self.textsScore = dict()
        self.faceScore = 0.0
        self.finalScore = 0.0

with open(Path('MockupFiles/captionMOC_3.txt'), 'r') as f: #TODO modify moc file
    caption = f.read().replace('\n', '')
sPost = ScoringPost('0', caption)

def __unpack_post_for_comprehend(sPost: ScoringPost):
    return list([sPost.caption, *sPost.texts.values()])
#BASTA CREARE MOCKS PER CAPTION E TEXTS


#sPost.text OTTENUTI DA:
def _parse_text_on_image(sPost: ScoringPost):
    with open(Path('MockupFiles/textOnPictureMOC_1_pizzaLab_ferragosto.json'), 'r') as f:
        textOnPicture = json.load(f)
    for line in textOnPicture['TextDetections']:
        if line['Type'] == 'LINE':
            sPost.texts[line['Id']] = line['DetectedText']


#CHI LA USA?
def __parse_comprehend_response(sPost: ScoringPost, compResult):
    n_texts = len(sPost.texts)
    if len(compResult['ErrorList']) > 0:
        raise Exception(compResult['ErrorList'])
    # se ErrorList vuota allora per ogni risultato nella lista dei risultati:
    for item in compResult['ResultList']:
        idx = item['Index']
        score = Score(item["Sentiment"])
        float_score = (
            item["SentimentScore"]["Positive"] - item["SentimentScore"]["Negative"]
            if (score != Score.MIXED)  #PER EVITARE DI CONSIDERARE "LUNEDI APERTO" ET SIMILA?
            else 0.0
        )
        if idx == 0:
            sPost.captionScore = float_score
        else:
            sPost.textsScore[idx - 1] = float_score

def _runComprehend(sPost: ScoringPost):
    _comprehend = boto3.client(
        service_name='comprehend', region_name='eu-central-1'
    )
    TextList = __unpack_post_for_comprehend(sPost)
    response = _comprehend.batch_detect_sentiment(TextList = TextList, LanguageCode = 'en') 
    __parse_comprehend_response(sPost, response)



__unpack_post_for_comprehend(sPost)
_runComprehend(sPost)

