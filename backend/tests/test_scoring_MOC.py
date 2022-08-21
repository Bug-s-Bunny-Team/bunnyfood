def _calcFinalScore(sPost: ScoringPost):
    sPost.faceScore = 69  #SCORE DA facialAnalysisMOC.json
    sPost.finalScore = (
        (
            sPost.captionScore
            + sPost.faceScore
            + sum(sPost.textsScore.values()) / len(sPost.textsScore)
        )
        / 2.0
        if len(sPost.textsScore) != 0
        else sPost.captionScore
    )

def _printAllScores(sPost: ScoringPost):
    print('Print all scores: {')
    print('textsScore=', sPost.textsScore)
    print('captionScore=', sPost.captionScore)
    print('faceScore=', sPost.faceScore)
    print('finalScore=', sPost.finalScore)
    print('}')

