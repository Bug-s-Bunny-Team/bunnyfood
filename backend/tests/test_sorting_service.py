from unittest import TestCase

from botocore.stub import Stubber

from entity.image import Image
from entity.post import Post
from functions.sorter.function.sorting_service import SorterService


class TestSorterService(TestCase):
    def setUp(self):
        self.sorting_service = SorterService()
        self.reko = self.sorting_service._rekognition
        self.comp = self.sorting_service._comprehend

    def test_calculate_text_score(self):
        with Stubber(self.reko) as rekogntion_stubber:
            detect_faces_response = {
                "FaceDetails": [
                    {
                        "Emotions": [
                            {
                                "Type": "SAD",
                                "Confidence": 99.99238586425781
                            },
                            {
                                "Type": "SURPRISED",
                                "Confidence": 6.682539939880371
                            },
                            {
                                "Type": "FEAR",
                                "Confidence": 6.06709098815918
                            },
                            {
                                "Type": "ANGRY",
                                "Confidence": 1.5936696529388428
                            },
                            {
                                "Type": "DISGUSTED",
                                "Confidence": 1.531591534614563
                            },
                            {
                                "Type": "CALM",
                                "Confidence": 1.116552710533142
                            },
                            {
                                "Type": "HAPPY",
                                "Confidence": 0.9199422001838684
                            },
                            {
                                "Type": "CONFUSED",
                                "Confidence": 0.379514217376709
                            }
                        ]},
                    {
                        "Emotions": [
                            {
                                "Type": "HAPPY",
                                "Confidence": 99.20760345458984
                            },
                            {
                                "Type": "SURPRISED",
                                "Confidence": 6.340514183044434
                            },
                            {
                                "Type": "FEAR",
                                "Confidence": 5.936931610107422
                            },
                            {
                                "Type": "SAD",
                                "Confidence": 2.1777870655059814
                            },
                            {
                                "Type": "CONFUSED",
                                "Confidence": 0.12417789548635483
                            },
                            {
                                "Type": "DISGUSTED",
                                "Confidence": 0.09452683478593826
                            },
                            {
                                "Type": "ANGRY",
                                "Confidence": 0.06957276910543442
                            },
                            {
                                "Type": "CALM",
                                "Confidence": 0.06028551235795021
                            }

                        ]}
                ]}
            detect_labels_response = {
                "Labels": [

                    {
                        "Name": "Person",
                        "Confidence": 99.88428497314453,
                        "Instances": [
                            {
                                "BoundingBox": {
                                    "Width": 0.27858132123947144,
                                    "Height": 0.44550982117652893,
                                    "Left": 0.2236727923154831,
                                    "Top": 0.35303789377212524
                                },
                                "Confidence": 99.88428497314453
                            },
                            {
                                "BoundingBox": {
                                    "Width": 0.20297367870807648,
                                    "Height": 0.6778767108917236,
                                    "Left": 0.5247262716293335,
                                    "Top": 0.10922279208898544
                                },
                                "Confidence": 99.81658172607422
                            },
                            {
                                "BoundingBox": {
                                    "Width": 0.1879337579011917,
                                    "Height": 0.6780399084091187,
                                    "Left": 0,
                                    "Top": 0.2805716097354889
                                },
                                "Confidence": 99.4343490600586
                            },
                            {
                                "BoundingBox": {
                                    "Width": 0.1857394129037857,
                                    "Height": 0.7207215428352356,
                                    "Left": 0.8122804164886475,
                                    "Top": 0.26372382044792175
                                },
                                "Confidence": 99.33649444580078
                            },
                            {
                                "BoundingBox": {
                                    "Width": 0.3435731828212738,
                                    "Height": 0.5872151255607605,
                                    "Left": 0.6002987623214722,
                                    "Top": 0.37104183435440063
                                },
                                "Confidence": 99.21895599365234
                            },
                            {
                                "BoundingBox": {
                                    "Width": 0.04421132802963257,
                                    "Height": 0.0647316426038742,
                                    "Left": 0.21105122566223145,
                                    "Top": 0.4905780255794525
                                },
                                "Confidence": 77.19906616210938
                            },
                            {
                                "BoundingBox": {
                                    "Width": 0.24612759053707123,
                                    "Height": 0.649583101272583,
                                    "Left": 0.5614517331123352,
                                    "Top": 0.21997611224651337
                                },
                                "Confidence": 63.90801239013672
                            }
                        ],
                        "Parents": []
                    }]
            }

            rekogntion_stubber.add_response("detect_labels", detect_labels_response,
                                            {'Image': {'S3Object': {'Bucket': 'test-bucket-backend-bugsbunny',
                                                                    'Name': '15.jpg'}}, 'MaxLabels': 10})

            rekogntion_stubber.add_response("detect_faces", detect_faces_response,
                                            {'Attributes': ['ALL'],
                                             'Image': {'S3Object': {'Bucket': 'test-bucket-backend-bugsbunny',
                                                                    'Name': '15.jpg'}}})
            img = Image("15.jpg")
            post = Post(id=5, caption="testo", image_key='iii54', list_images=[img])
            self.sorting_service.calculate_image_score(post)
            print(post.imageScore)
            self.assertEqual(60, post.imageScore, 'score wrong')

    def test_calculate_image_score(self):
        # Da implementare
        return 1

    def test_sort(self):
        # Da implementare
        return 1
