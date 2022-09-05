from types import SimpleNamespace
from unittest import TestCase
from pathlib import Path
import json


class TestSorter(TestCase):
    def test_setup(self):
        with open(Path('fixtures/reko_analysis_couple_restaurant.json'), 'r') as file:
            data = json.load(file, object_hook=lambda d: SimpleNamespace(**d))

            data_test = data.Labels[0]

            # param: expected, actual, msg in case of error
            self.assertEqual(data_test, data_test, 'wrong_analysis')
