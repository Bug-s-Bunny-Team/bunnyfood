import json
import pytest
from pathlib import Path
from sqlalchemy.orm import Session
from functions.scoring.function.models import ScoringPost
from functions.scoring.function.scoring_service import BasicScoringService


'''@pytest.fixture
def scorer(session):
    return BasicScoringService(session)'''

@pytest.fixture
def scorer():
    session = Session()
    return BasicScoringService(session)

@pytest.fixture
def scored():
    return ScoringPost('0', 'ab', '0', {0: ''})


def load_json_fixture(path: str) -> dict:

    path = '../tests/fixtures' / Path(path)
    with open(path, 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("face_score, texts_score, caption_score, expected_final_score",[
    (1,{0:1},1,5),
    (0,{0:-1},-1,0),
    (0.5,{0:0},0,2.5)
])
def test_calcFinalScore_all_present(scorer, scored, face_score, texts_score, caption_score, expected_final_score):
    sPost = scored
    sPost.faceScore = face_score
    sPost.textsScore = texts_score
    sPost.captionScore = caption_score
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore

    assert score == expected_final_score

def test_calcFinalScore_all_missing(scorer, scored):
    sPost = scored
    sPost.caption = ' '
    sPost.textsScore = {}
    sPost.faceScore = None
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore

    assert score is None

@pytest.mark.parametrize("face_score, texts_score, caption_score, caption, expected_final_score",[
    (1,{},None,' ', 5),
    (None, {0:1}, None, ' ', 5),
    (None, {}, 1, 'aba', 5)
])
def test_calcFinalScore_one_present(scorer, scored, face_score, texts_score, caption_score, caption, expected_final_score):
    sPost = scored
    sPost.caption=caption
    sPost.faceScore = face_score
    sPost.textsScore = texts_score
    sPost.captionScore = caption_score
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore

    assert score == expected_final_score

@pytest.mark.parametrize("face_score, texts_score, caption_score, caption, expected_final_score", [
    (1, {0:1}, None, ' ', 5),
    (1, {}, 1, 'aba', 5),
    (None, {0:1}, 1, 'aba', 5)
])
def test_calcFinalScore_two_present(scorer, scored, face_score, texts_score, caption_score, caption, expected_final_score):
    sPost = scored
    sPost.caption = caption
    sPost.faceScore = face_score
    sPost.textsScore = texts_score
    sPost.captionScore = caption_score
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore

    assert score == expected_final_score

@pytest.mark.parametrize("face_result_path, expected_score", [
    ("facialAnalysisMOC_empty.json", None),
    ("facialAnalysisMOC_max_happy.json",1),
])
def test_face_scoring(scorer, scored, face_result_path, expected_score):
    '''
    TODO:   face empty
            face all not valid
            face max happy
            face max calm
            face mid happy mid disgust
    '''
    sPost = scored
    text_result={}
    face_result=load_json_fixture(face_result_path)
    scorer.__parse_rekognition_response(sPost,text_result,face_result)
    '''error: BasicScoringService object has no attribute __parse_rekognition_response'''

    assert sPost.faceScore == expected_score

