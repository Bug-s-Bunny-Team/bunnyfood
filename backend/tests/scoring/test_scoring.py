import pytest
from sqlalchemy.orm import Session

from functions.scoring.function.models import ScoringPost
from functions.scoring.function.scoring_service import BasicScoringService

'''class RekoMock(ClientMock):
    def __init__(
        self,
        detect_faces_resp: str = 'detect_faces.json',
        detect_labels_resp: str = 'detect_labels.json',
        detect_text_resp: str = 'detect_text.json'
    ):
        self.detect_faces_resp = detect_faces_resp
        self.detect_labels_resp = detect_labels_resp
        self.detect_text_resp = detect_text_resp

    def detect_faces(self, *args, **kwargs):
        return self.load_json_fixture(self.detect_faces_resp)

    def detect_labels(self, *args, **kwargs):
        return self.load_json_fixture(self.detect_labels_resp)

    def detect_text(self, *args, **kwargs):
        return self.load_json_fixture(self.detect_text_resp)
'''


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
def test_calcFinalScore_two_present(scorer, scored, face_score, texts_score, caption_score, caption,
                                    expected_final_score):
    sPost = scored

    sPost.caption = caption
    sPost.faceScore = face_score
    sPost.textsScore = texts_score
    sPost.captionScore = caption_score
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore
    assert score == expected_final_score
