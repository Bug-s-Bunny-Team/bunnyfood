# commento è relativo alla riga a lui sottostante

import boto3
import os
from abc import ABC, abstractmethod
from .models import ScoringPost, Score
from .event_adapter import EventAdapter
from .output_strategy import OutputStrategy


class ScoringService(ABC):
    __e: EventAdapter
    __o: OutputStrategy
    _rekognition = boto3.client(
        service_name='rekognition', region_name=os.environ['ENV_REGION_NAME']
    )
    _comprehend = boto3.client(
        service_name='comprehend', region_name=os.environ['ENV_REGION_NAME']
    )

    def __init__(self, e: EventAdapter, o: OutputStrategy):
        self.__e = e
        self.__o = o

    def score(self, event):
        sPost = self.__e.processEvent(event)
        self._runRekognition(sPost)
        self._runComprehend(sPost)
        self._calcFinalScore(sPost)
        self.__o.output(sPost)

    @abstractmethod
    def _runRekognition(self, sPost: ScoringPost):
        pass

    @abstractmethod
    def _runComprehend(self, sPost: ScoringPost):
        pass

    @abstractmethod
    def _calcFinalScore(self, sPost: ScoringPost):
        pass


class BasicScoringService(ScoringService):
    def __parse_rekognition_response(self, sPost: ScoringPost, rekResult):
        for line in rekResult['TextDetections']:
            if line['Type'] == 'LINE':
                sPost.texts[line['Id']] = line['DetectedText']
        # FACE SCORE
        # aggiungere Spost.faceScore = somenthing

    def __unpack_post_for_comprehend(self, sPost: ScoringPost):
        return list([sPost.caption, *sPost.texts.values()])

    # SCORING
    # qui vengono fatti gli scoring per caption(diretto) e text on image(preso da reko)
    def __parse_comprehend_response(self, sPost: ScoringPost, compResult):
        n_texts = len(sPost.texts)
        if len(compResult['ErrorList']) > 0:
            raise Exception(compResult['ErrorList'])
        # se ErrorList vuota allora per ogni risultato nella lista dei risultati:
        for item in compResult['ResultList']:
            idx = item['Index']
            score = Score(item["Sentiment"])
            # sentimentScore ha 4 campi con un valore ciascuno (sommati danno 1)
            # ovvero: Positive, Negative, Neutral, Mixed
            # valori per ogni campo =[0,1]
            # score= differenza(positivo,negativo)
            # se mixed, score=0 perche' non significativo
            float_score = (
                item["SentimentScore"]["Positive"] - item["SentimentScore"]["Negative"]
                if (score != Score.MIXED)
                else 0.0
            )
            if idx == 0:
                sPost.captionScore = float_score
            else:
                sPost.textsScore[idx - 1] = float_score

    def __parse_dominant_language_response(self, domResponse):
        return (
            domResponse['Languages'][0]['LanguageCode']
            if domResponse['Languages'][0]
            else 'en'
        )

    def _runRekognition(self, sPost: ScoringPost):
        print('Analyzing image')
        response = self._rekognition.detect_text(
            Image={
                'S3Object': {
                    'Bucket': os.environ['ENV_BUCKET_NAME'],
                    'Name': sPost.image,
                }
            }
        )
        BasicScoringService.__parse_rekognition_response(sPost, response)
        # ADD NEW RESPONSE
        # response = self._rekognition.facial_analysis(Image={'S3Object': {'Bucket': os.environ['ENV_BUCKET_NAME'], 'Name': sPost.image}})
        # BasicScoringService.__parse_rekognition_response(sPost, response)

        print('Successfully analized image')

    def _runComprehend(self, sPost: ScoringPost):
        print('Analizying textual information')
        dominantLanguageResponse = self._comprehend.detect_dominant_language(
            Text=sPost.caption
        )
        response = self._comprehend.batch_detect_sentiment(
            TextList=BasicScoringService.__unpack_post_for_comprehend(sPost),
            LanguageCode=BasicScoringService.__parse_dominant_language_response(
                dominantLanguageResponse
            ),
        )
        BasicScoringService.__parse_comprehend_response(sPost, response)
        print('Successfully analized textual information')

    def _calcFinalScore(self, sPost: ScoringPost):
        # aggiungere sPost.faceScore
        # aggiornare sPost aggiungendoci faceScore
        sPost.finalScore = (
            (
                sPost.captionScore
                + sum(sPost.textsScore.values()) / len(sPost.textsScore)
            )
            / 2.0
            if len(sPost.textsScore) != 0
            else sPost.captionScore
        )
