from typing import Dict

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


#sPost = ScoringPost('0', '')    # C VUOTA
sPost = ScoringPost('0', 'uhs') # C

#sPost.textsScore ={}            # T VUOTA
sPost.textsScore = {0: 0.1}     # T

#sPost.faceScore =None           # F VUOTA
sPost.faceScore =7              # F



#SE F,T VUOTE ok
if sPost.faceScore == None and len(sPost.textsScore) == 0:
    print('F,T vuote')
# SE C,T VUOTE ok
elif not (sPost.caption and not sPost.caption.isspace()) and len(sPost.textsScore) == 0:
    print('C,T vuote')
# SE F,C VUOTE ok
elif sPost.faceScore == None and not (sPost.caption and not sPost.caption.isspace()):
    print('F,C vuote')
# SE T VUOTA ok
elif len(sPost.textsScore) == 0:
    print('T vuota')
# SE F VUOTA ok
elif sPost.faceScore == None:
    print('F vuota')
# SE C VUOTA ok
elif not (sPost.caption and not sPost.caption.isspace()):
    print('C vuota')
# SE NESSUNA VUOTA ok
else:
    print('nessuna vuota')
