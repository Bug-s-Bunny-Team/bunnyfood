import json
from pathlib import Path

def scoreFaceRekognition():
    with open(Path('facialAnalysisMOC.json'),'r') as f:
        response = json.load(f)

    faceCount = 0
    scoreSum = 0


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
    totScore = scoreSum / faceCount
    print('Facce analizzate=', faceCount)
    print('Score Immagine=' ,totScore)

scoreFaceRekognition()

'''
# CODICE PER DEBUG
for face in response['FaceDetails']:
    pose = face['Pose']
    #print(pose['Yaw'], pose['Pitch'])
    #SE VOLTO DRITTO
    if (abs(pose['Yaw']) <= 50) and (abs(pose['Pitch']) <= 50): #abs() perchè deve essere -50<pose<50
        #CALCOLARE SCORE EMOZIONI
        faceCount = faceCount + 1
        #print('Volto valido num=', faceCount)
        faceSum = 0
        disgusted = False
        for emotion in face['Emotions']:
            if emotion['Type'] == 'HAPPY':
                faceSum = faceSum + emotion['Confidence']
                #print('HAPPY=', emotion['Confidence'])
                #print('faceSum=', faceSum)
            if emotion['Type'] == 'CALM':
                faceSum = faceSum + emotion['Confidence']*0.5 #ha peso minore di happy
                #print('CALM=', emotion['Confidence'])
                #print('faceSum=', faceSum)
            if emotion['Type'] == 'DISGUSTED':
                if emotion['Confidence'] >= 50: #se disgust troppo elevato azzera il punteggio della faccia
                    disgusted = True
                    #print('Too much digust=', emotion['Confidence'])
        if disgusted == False:
            scoreSum = scoreSum + faceSum #se volto disgusted value >= allora face value = 0
        #print('scoreSum=', scoreSum)
    #UN VOLTO STORTO VIENE IGNORATO NEL CALCOLO
'''
