from unittest import TestCase
from mlapp.main.nlp import TrainingData as td


class TestTrainingData(TestCase):

    def test_topic_name(self):
        test_td = td.TrainingData('test_user', 'Test_topic', 'none')
        self.assertTrue(test_td.topic_name == 'test_topic')

    def test_add_annotator(self):
        test_td = td.TrainingData('test_user', 'Test_topic', 'none')
        test_td.add_annotator('Snow')
        test_td.add_annotator('john')
        self.assertTrue(test_td.annotators == ['Snow', 'john'])

    def test_get_annotators(self):
        test_td = td.TrainingData('test_user', 'Test_topic', 'none')
        test_td.add_annotator('Snow')
        test_td.add_annotator('john')
        self.assertTrue(test_td.get_annotators() == ['Snow', 'john'])


