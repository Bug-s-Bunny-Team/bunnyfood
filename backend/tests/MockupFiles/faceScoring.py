import json
from pathlib import Path

def scoreFaceRekognition():
    with open(Path('facialAnalysisMOC.json'),'r') as f:
        response = json.load(f)

    '''###############################################
    for line in rekResult['TextDetections']:
        if line['Type'] == 'LINE':
            sPost.texts[line['Id']] = line['DetectedText']
    ###############################################'''

    faceCount=0
    scoreSum=0

    '''for face in response['FaceDetails']:
        for emotion in face['Emotions']:
            if emotion['Type'] == 'HAPPY':
                #SOMMA LA CONFIDENCE DI HAPPY PER OGNI FACCIA
                #scoreSum = scoreSum + emotion['Confidence']
                print(emotion['Confidence'])
                #faceCount=faceCount+1'''

    for face in response['FaceDetails']:
        pose = face['Pose']
        print(pose['Yaw'], pose['Pitch'])
        #SE VOLTO DRITTO
        if (abs(pose['Yaw']) <= 50) and (abs(pose['Pitch']) <= 50): #abs() perchè deve essere -50<pose<50
            #CALCOLARE SCORE EMOZIONI
            faceCount = faceCount + 1
            print('Volto valido num=', faceCount)
            for emotion in face['Emotions']:
                if emotion['Type'] == 'HAPPY':
                    scoreSum = scoreSum + emotion['Confidence']
                    print(emotion['Confidence'])
                if emotion['Type'] == 'CALM':
                    scoreSum = scoreSum + emotion['Confidence']*0.5
                    print(emotion['Confidence'])
        #UN VOLTO STORTO VIENE IGNORATO NEL CALCOLO




    #totScore = scoreSum / faceCount
    #print(totScore)


scoreFaceRekognition()