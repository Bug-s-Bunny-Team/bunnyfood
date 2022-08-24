from unittest import TestCase

from functions.sorter.function.models import Post, Image
from functions.sorter.function.sorting_service import SorterService

img = Image("15.jpg")
bucket = 'test-bucket-backend-bugsbunny'


# post = Post(id=5, caption="bel posto e buon cibo", list_images=[img])
class TestSorterService(TestCase):
    def setUp(self):
        self.sorting_service = SorterService()
        self.reko = self.sorting_service._rekognition
        self.comp = self.sorting_service._comprehend

    def test_detect_language_text(self):
        print('start test_detect_language_text')
        # per provare inglese(i am a man and i have 52 years)
        text = 'vediamo se capisci di cosa parlo'
        language = self.sorting_service.detect_language_text(text)
        print(language)
        self.assertEqual('it', language, 'test_detect_language_text failed')
        print('finish test_detect_language_text')

    def test_detect_sentiment_text(self):
        print('start test_detect_sentiment_text')
        language = 'it'
        post = Post(id=5, caption="bel posto e buon cibo ma sono rimasto deluso dal servizio. Primi fantastici, "
                                  "secondi un po meno. Prezzo nella mdedia", list_images=[img])

        score = self.sorting_service.detect_sentiment_text(post, language)
        post.set_caption_score(score)
        post.calculate_final_score()
        print(post.finalScore)
        self.assertEqual(9.9, post.finalScore, 'test_detect_sentiment_text')
        print('finish test_detect_sentiment_text')

    def test_detect_person(self):
        print('start test_detect_person')
        response = {
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

        contain_person = False

        for label in response['Labels']:
            if label['Confidence'] >= 90:
                if label['Name'] == 'Person':
                    contain_person = True
        if contain_person:
            print(contain_person)
            self.assertEqual(1, contain_person)
            print('finish test_detect_person')
            return contain_person
        else:
            print('no person in image')
            self.assertEqual(0, contain_person)
            print('finish test_detect_person')

    def test_detect_sentiment_person(self):
        print('start test_detect_sentiment_person')
        response = {"FaceDetails": [{"Emotions": [{"Type": "HAPPY", "Confidence": 95}], "Confidence": 99}]}
        contain_emotion = False
        emotions_dict = {}
        emotions_confid = []

        for faceDetail in response['FaceDetails']:
            emotions = faceDetail['Emotions']
            confid_single_face = {}
            for emotion in emotions:
                emotion_name = emotion['Type']
                emotion_confid_value = emotion['Confidence']
                if emotion_name != 'UNKNOWN':
                    confid_single_face[emotion_name] = emotion_confid_value
                    if emotion_confid_value >= 90:
                        if emotion_name in emotions_dict:
                            emotions_dict[emotion_name] += 1
                        else:
                            emotions_dict[emotion_name] = 1
                        contain_emotion = True
            emotions_confid.append(confid_single_face)

        if contain_emotion:
            print(contain_emotion)
            print('Emozioni')
            print(emotions_dict)
            print('Grado Emozioni')
            print(emotions_confid)
            self.assertEqual(1, contain_emotion)
            print('finish test_detect_sentiment_person')
            return emotions_dict, contain_emotion, emotions_confid
        else:
            print('no emotions')
            self.assertEqual(0, contain_emotion)
            print('finish test_detect_sentiment_person')

    def test_analyze_image(self):
        print('start test_analyze_image')
        emotions = {}
        emotions_confidence = {}

        contain_person = self.test_detect_person()
        if contain_person:
            print("There is a person")
            emotions, contain_emotion, emotions_confidence = self.test_detect_sentiment_person()
            if contain_emotion:
                print("Emotion detected")
                print('È VIVOOOOO')
                self.assertEqual(1, contain_emotion)
                print('finish test_analyze_image')
                return emotions, emotions_confidence
            else:
                print("No emotion detected")
                self.assertEqual(0, contain_emotion)
                print('finish test_analyze_image')
        else:
            print("There is no person")
            self.assertEqual(0, contain_person)
            print('finish test_analyze_image')

    def test_calculate_text_score(self):
        print('start test_calculate_text_score')
        post = Post(id=5, caption="bel posto e buon cibo", list_images=[img])

        if post.caption:
            score = self.sorting_service.detect_sentiment_text(post,
                                                               self.sorting_service.detect_language_text(post.caption))
            post.set_caption_score(score)
            post.calculate_final_score()

            print("\n")
            print('Print Final Score')
            print(post.finalScore)
            self.assertEqual(99, post.finalScore, 'test_calculate_text_score failed')
            print('finish test_calculate_text_score')
            return post.finalScore
        else:
            print('test_calculate_text_score failed')
            self.fail() # sostituire con self.assertEqual
            print('finish test_calculate_text_score')

    def test_calculate_image_score(self):
        print('start test_calculate_image_score')
        post = Post(id=5, caption="bel posto e buon cibo", list_images=[img])
        if post.list_images:
            for image in post.list_images:
                image_name = image.name
                print("image name " + image_name)
                emotions, emotions_confidence = self.test_analyze_image()

                image.set_emotions(emotions)
                image.set_emotions_confidence(emotions_confidence)
        else:
            print('no image in post')
            self.assertEqual(0, post.list_images)
            print('finish test_calculate_image_score')

        post.calculate_and_set_image_score()
        print(post.imageScore)
        self.assertEqual(100, post.imageScore)
        print('finish test_calculate_image_score')
        return post.imageScore

    def test_sort(self):
        print('start test_sort')
        text_score = self.test_calculate_text_score()
        if not text_score:
            print('no text found')
        image_score = self.test_calculate_image_score()
        if image_score is not None or text_score is not None:
            print('save post')
            self.assertEqual(100, image_score)
            print('finish test_sort')
        else:
            print('delete post')
            self.assertEqual(0, image_score)
            print('finish test_sort')

