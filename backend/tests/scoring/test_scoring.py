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


@pytest.fixture
def scorer():
    session = Session()
    return BasicScoringService(session)


@pytest.fixture
def scored():
    return ScoringPost('0', 'ab', '0', {0: ''})


def test_calcFinalScore(scorer, scored):
    '''
    TODO:   all max score
            all min score
            one max rest none (foreach)
            all none
            FOR NOW STOP
    '''
    sPost = scored

    sPost.faceScore = 1
    sPost.textsScore = {0: 1}
    sPost.captionScore = 1
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore
    assert score == 5

    sPost.faceScore = 0
    sPost.textsScore = {0: -1}
    sPost.captionScore = -1
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore
    assert score == 0
