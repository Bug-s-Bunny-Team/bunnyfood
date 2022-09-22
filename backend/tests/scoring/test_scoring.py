import json
from pathlib import Path

import pytest
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


@pytest.mark.parametrize(
    "face_score, texts_score, caption_score, expected_final_score",
    [(1, {0: 1}, 1, 5), (0, {0: -1}, -1, 0), (0.5, {0: 0}, 0, 2.5)],
)
def test_calcFinalScore_all_present(
    scorer, scored, face_score, texts_score, caption_score, expected_final_score
):
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


@pytest.mark.parametrize(
    "face_score, texts_score, caption_score, caption, expected_final_score",
    [(1, {}, None, ' ', 5), (None, {0: 1}, None, ' ', 5), (None, {}, 1, 'aba', 5)],
)
def test_calcFinalScore_one_present(
    scorer,
    scored,
    face_score,
    texts_score,
    caption_score,
    caption,
    expected_final_score,
):
    sPost = scored
    sPost.caption = caption
    sPost.faceScore = face_score
    sPost.textsScore = texts_score
    sPost.captionScore = caption_score
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore

    assert score == expected_final_score


@pytest.mark.parametrize(
    "face_score, texts_score, caption_score, caption, expected_final_score",
    [(1, {0: 1}, None, ' ', 5), (1, {}, 1, 'aba', 5), (None, {0: 1}, 1, 'aba', 5)],
)
def test_calcFinalScore_two_present(
    scorer,
    scored,
    face_score,
    texts_score,
    caption_score,
    caption,
    expected_final_score,
):
    sPost = scored
    sPost.caption = caption
    sPost.faceScore = face_score
    sPost.textsScore = texts_score
    sPost.captionScore = caption_score
    scorer._calcFinalScore(sPost)
    score = sPost.finalScore

    assert score == expected_final_score


@pytest.mark.parametrize(
    "face_result_path, expected_score",
    [
        ("facialAnalysisMOC_empty.json", None),
        ("facialAnalysisMOC_all_not_valid.json", None),
        ("facialAnalysisMOC_max_happy.json", 1),
        ("facialAnalysisMOC_max_calm.json", 0.5),
        ("facialAnalysisMOC_half_happy_half_disgusted.json", 0),
    ],
)
def test_face_scoring(scorer, scored, face_result_path, expected_score):
    sPost = scored
    text_result = load_json_fixture('textOnPictureMOC_empty.json')
    face_result = load_json_fixture(face_result_path)
    scorer._BasicScoringService__parse_rekognition_response(
        sPost, text_result, face_result
    )

    assert sPost.faceScore == expected_score


@pytest.mark.parametrize(
    "text_result_path, expected_text",
    [
        ("textOnPictureMOC_empty.json", {}),
        ("textOnPictureMOC_not_empty.json", {0: 'FIRST', 1: 'SECOND', 2: 'THIRD'}),
    ],
)
def test_text_on_picture(scorer, scored, text_result_path, expected_text):
    sPost = scored
    text_result = load_json_fixture(text_result_path)
    face_result = load_json_fixture("facialAnalysisMOC_empty.json")
    scorer._BasicScoringService__parse_rekognition_response(
        sPost, text_result, face_result
    )

    assert sPost.texts == expected_text


@pytest.mark.parametrize(
    "comprehend_result_path, expected_score",
    [
        ("comprehendCaptionResultMOC_positive.json", 1),
        ("comprehendCaptionResultMOC_negative.json", -1),
        ("comprehendCaptionResultMOC_neutral.json", 0),
    ],
)
def test_caption_scoring(scorer, scored, comprehend_result_path, expected_score):
    sPost = scored
    comprehend_result = load_json_fixture(comprehend_result_path)
    scorer._BasicScoringService__parse_comprehend_response(sPost, comprehend_result)

    assert sPost.captionScore == expected_score


@pytest.mark.parametrize(
    "comprehend_result_path, expected_score",
    [
        ("comprehendTextsResultMOC_positive.json", {0: 1, 1: 1, 2: 1}),
        ("comprehendTextsResultMOC_negative.json", {0: -1, 1: -1, 2: -1}),
        ("comprehendTextsResultMOC_neutral.json", {0: 0, 1: 0, 2: 0}),
    ],
)
def test_caption_scoring(scorer, scored, comprehend_result_path, expected_score):
    sPost = scored
    comprehend_result = load_json_fixture(comprehend_result_path)
    scorer._BasicScoringService__parse_comprehend_response(sPost, comprehend_result)

    assert sPost.textsScore == expected_score
