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
    faceScore: float
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
    #print('no input moc')
    #moc = '1'
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
    elif moc == '4':
        print('Scelta caption vuota, textOnPicture pizza lab ferragosto')
        captionPath = 'MockupFiles/captionMOC_empty.txt'
        textOnPicturePath = 'MockupFiles/textOnPictureMOC_1_pizzaLab_ferragosto.json'
    elif moc == '5':
        print('Scelta caption riscritta, textOnPicture vuota')
        captionPath = 'MockupFiles/captionMOC_3.txt'
        textOnPicturePath = 'MockupFiles/textOnPictureMOC_empty.json'
    else:
        print('not valid')

###SCEGLIE MOC################
_chooseMOC()
##############################


###ISTANZIA sPost########################
with open(Path(captionPath), 'r') as f:
    caption = f.read().replace('\n', '')
sPost = ScoringPost('0', caption)
#######################################

def __unpack_post_for_comprehend(sPost: ScoringPost):
    return list([sPost.caption, *sPost.texts.values()])


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
            if float_score <-1 or float_score > 1:
                raise Exception('captionScore invalid')
            sPost.captionScore = float_score
            print('captionScore=', float_score) #caption score è una sola
        else:
            if float_score <-1 or float_score > 1:
                raise Exception('textScore invalid')
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

def _scoreFaceRekognition(sPost: ScoringPost):
    with open(Path('MockupFiles/facialAnalysisMOC_4.json'), 'r') as f:
        response = json.load(f)

    faceCount = 0
    scoreSum = 0

    print(len(response['FaceDetails']))

    if len(response['FaceDetails']) > 0: #controlla ci siano volti nell'immagine
        for face in response['FaceDetails']:
            pose = face['Pose']
            #SE VOLTO DRITTO
            if (abs(pose['Yaw']) <= 50) and (abs(pose['Pitch']) <= 50): #abs() perchè deve essere -50<pose<50
                #CALCOLARE SCORE EMOZIONI
                faceCount = faceCount + 1
                faceSum = 0
                disgusted = False
                for emotion in face['Emotions']:
                    if emotion['Type'] == 'HAPPY':
                        faceSum = faceSum + emotion['Confidence']
                    if emotion['Type'] == 'CALM':
                        faceSum = faceSum + emotion['Confidence']*0.5 #ha peso minore di happy
                    if emotion['Type'] == 'DISGUSTED':
                        if emotion['Confidence'] >= 50: #se disgust troppo elevato azzera il punteggio della faccia
                            disgusted = True
                if disgusted == False:
                    scoreSum = scoreSum + faceSum #se volto disgusted value >= allora face value = 0
            #UN VOLTO STORTO VIENE IGNORATO NEL CALCOLO
        faceScore = (scoreSum / faceCount) # =[0,100]
        if faceScore < 0 or faceScore > 100:
            raise Exception('faceScore invalid')
        sPost.faceScore = faceScore / 100  # =[0,1]
    else:
        sPost.faceScore = None #se non ci sono facce metto nullo il facescore

    print('Facce analizzate=', faceCount)
    print('Score Immagine=' ,sPost.faceScore)


def _calcFinalScore(sPost: ScoringPost):
    #final score= [0,5] con scarti di 0.5     (se presenti tutti e tre i valori)
    #composta così:   -2 punti per caption score
    #                 -2 punti per face score
    #                 -1 punto per text on image score

    #se presente del text on screen normalizzo la sua (loro) score
    if len(sPost.textsScore) != 0:
        textScore = sum(sPost.textsScore.values()) / len(sPost.textsScore)  # =[-1,1]
        normalizedTextScore = (textScore + 1) / 2  # =[0,1]

    #se presente la caption normalizzo la sua score
    if sPost.caption and not sPost.caption.isspace():
        normalizedCaptionScore = (sPost.captionScore +1) / 2 # =[0,1]

    # face score è già =[0,1]

    #CALCOLO DI FINAL SCORE
    #F,T,C = faceScore, textScore, captionScore
    #vuote = post analizzato non contiene: volti(F), testo a schermo(T), caption(C)
    #SE TUTTE VUOTE
    if not (sPost.caption and not sPost.caption.isspace()) and len(sPost.textsScore) == 0 and sPost.faceScore == None:
        sPost.finalScore = None
    #SE F,T VUOTE
    elif sPost.faceScore == None and len(sPost.textsScore) == 0:
        sPost.finalScore = (
            normalizedCaptionScore * 5
        )
    #SE C,T VUOTE
    elif not(sPost.caption and not sPost.caption.isspace()) and len(sPost.textsScore) == 0:
        sPost.finalScore = (
            sPost.faceScore * 5
        )
    #SE F,C VUOTE
    elif sPost.faceScore == None and not(sPost.caption and not sPost.caption.isspace()):
        sPost.finalScore = (
            normalizedTextScore * 5
        )
    #SE T VUOTA
    elif len(sPost.textsScore) == 0:
        sPost.finalScore = (
            sPost.faceScore * 2.5
            + normalizedCaptionScore * 2.5
        )
    #SE F VUOTA
    elif sPost.faceScore == None:
        sPost.finalScore = (
            normalizedTextScore * 2
            + normalizedCaptionScore * 3
        )
    #SE C VUOTA
    elif not(sPost.caption and not sPost.caption.isspace()):
        sPost.finalScore = (
            sPost.faceScore * 3
            + normalizedTextScore * 2
        )
    #SE NESSUNA VUOTA
    else:
        sPost.finalScore = (
                normalizedCaptionScore * 2
                + sPost.faceScore * 2
                + normalizedTextScore
        )

def _setScores(sPost: ScoringPost):
    sPost.faceScore= 0.5                     #[0, 1]
    sPost.textsScore= {0: 0.0, 1: 0.0}     #[-1,1] * n
    sPost.captionScore= 0.0                 #[-1,1]

def _printAllScores(sPost: ScoringPost):
    print('Print all scores: {')
    textScore = sum(sPost.textsScore.values()) / len(sPost.textsScore)
    print('textScore=', textScore)
    print('captionScore=', sPost.captionScore)
    print('faceScore=', sPost.faceScore)
    print('finalScore=', sPost.finalScore)
    print('}')

_parse_text_on_image(sPost)
__unpack_post_for_comprehend(sPost)
_runComprehend(sPost)
_calcComprehendScore(sPost)
_scoreFaceRekognition(sPost)

#_setScores(sPost)
_calcFinalScore(sPost)
_printAllScores(sPost)
