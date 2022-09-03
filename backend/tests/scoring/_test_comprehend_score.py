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


captionPath = 'def'
textOnPicturePath = 'def'
def _chooseMOC():
    global captionPath
    global textOnPicturePath
    moc = input('Scegliere MOC')
    if moc == '1':
        print('Scelto pizza lab ferragosto')
        captionPath = 'MockupFiles/captionMOC_1_pizzaLab_ferragosto.txt'
        textOnPicturePath = 'MockupFiles/textOnPictureMOC_1_pizzaLab_ferragosto.json'
    elif moc == '2':
        print('Scelto corte dei ciliegi aperitivo')
        captionPath = 'MockupFiles/captionMOC_2_laCorte_apericorte.txt'
        textOnPicturePath = 'MockupFiles/textOnPictureMOC_2_laCorte_apericorte.json'
    elif moc == '3':
        print('Scelta caption riscritta, textOnPicture pizza lab ferragosto')
        captionPath = 'MockupFiles/captionMOC_3.txt'
        textOnPicturePath = 'MockupFiles/textOnPictureMOC_1_pizzaLab_ferragosto.json'
    else:
        print('not valid')

_chooseMOC()

with open(Path(captionPath), 'r') as f:
    caption = f.read().replace('\n', '')
sPost = ScoringPost('0', caption)


def __unpack_post_for_comprehend(sPost: ScoringPost):
    return list([sPost.caption, *sPost.texts.values()])
#BASTA CREARE MOCKS PER CAPTION E TEXTS


#sPost.text OTTENUTI DA:
def _parse_text_on_image(sPost: ScoringPost):
    global textOnPicturePath
    print('##########################################')
    print('_parse_text_on_image')
    with open(Path(textOnPicturePath), 'r') as f:
        textOnPicture = json.load(f)
    for line in textOnPicture['TextDetections']:
        if line['Type'] == 'LINE':
            sPost.texts[line['Id']] = line['DetectedText']
    print('textOnPicture post parse=', sPost.texts)
    print('##########################################')


#CHI LA USA?
def __parse_comprehend_response(sPost: ScoringPost, compResult):
    print('##########################################')
    print('__parse_comprehend_response')
    print('ANALISI SENTIMENT ALREADY DONE, ORA SI SCORA')
    #n_texts = len(sPost.texts) unused?
    if len(compResult['ErrorList']) > 0:
        raise Exception(compResult['ErrorList'])
    # se ErrorList vuota allora per ogni risultato nella lista dei risultati:
    for item in compResult['ResultList']:
        idx = item['Index']
        score = Score(item["Sentiment"])
        print('idx=', idx, ' score=', score)
        print('FLOAT SCORE =','POSITIVE(', item["SentimentScore"]["Positive"],')',
              ' - NEGATIVE(', item["SentimentScore"]["Negative"],')',
              ' = ', item["SentimentScore"]["Positive"] - item["SentimentScore"]["Negative"]
              )
        float_score = (
            item["SentimentScore"]["Positive"] - item["SentimentScore"]["Negative"]
            if (score != Score.MIXED)  #PER EVITARE DI CONSIDERARE "LUNEDI APERTO" ET SIMILA?
            else 0.0
        )
        if idx == 0:
            sPost.captionScore = float_score
            print('captionScore=', float_score) #caption score è una sola
        else:
            sPost.textsScore[idx - 1] = float_score #texts score fa una score per ogni pezzo di testo
            print('textsScore=', float_score)
    print('########################################')

def _runComprehend(sPost: ScoringPost):
    _comprehend = boto3.client(
        service_name='comprehend', region_name='eu-central-1'
    )
    TextList = __unpack_post_for_comprehend(sPost)
    print('TextList=', TextList)
    response = _comprehend.batch_detect_sentiment(TextList = TextList, LanguageCode = 'en')
    print("response batch detect sentiment=", response)
    __parse_comprehend_response(sPost, response)

def _calcComprehendScore(sPost: ScoringPost):
    sPost.finalScore = (
        (
                sPost.captionScore
                + sum(sPost.textsScore.values()) / len(sPost.textsScore)
        )
        / 2.0
        if len(sPost.textsScore) != 0
        else sPost.captionScore
    )
    print('FINAL SCORE =', sPost.finalScore)

_parse_text_on_image(sPost)
__unpack_post_for_comprehend(sPost)
_runComprehend(sPost)
_calcComprehendScore(sPost)
