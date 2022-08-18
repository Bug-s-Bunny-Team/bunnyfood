from types import SimpleNamespace
from unittest import TestCase
from pathlib import Path
import json


class TestSorter(TestCase):
    def test_setup(self):
        with open(Path('/Users/matte/Documents/GitHub/Università/bunnyfood/backend/tests/mockupFiles'
                       '/reko_analysis_couple_restaurant'), 'r') as file:
            data = json.load(file, object_hook=lambda d: SimpleNamespace(**d))

            data_test = data.Labels[0]

            # param: expected, actual, msg in case of error
            self.assertEqual(data_test, data_test, 'wrong_analysis')
