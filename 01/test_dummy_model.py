import unittest
from unittest.mock import patch

from dummy_model import predict_message_mood


class TestModel(unittest.TestCase):

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_5(self, mock_prediction):
        mock_prediction.return_value = 0.9
        self.assertEqual(predict_message_mood("Чапаев и пустота"), "отл")

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_34(self, mock_prediction):
        mock_prediction.return_value = 0.81
        self.assertEqual(predict_message_mood(
            "Чапаев и пустота", 0.8, 0.99), "норм")

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_2(self, mock_prediction):
        mock_prediction.return_value = 0.1
        self.assertEqual(predict_message_mood("Вулкан"), "неуд")

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_invalid_mes_type(self, mock_prediction):
        mock_prediction.return_value = 0.5
        with self.assertRaises(TypeError):
            predict_message_mood(777)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_invalid_thresholds_type(
            self, mock_prediction
    ):
        mock_prediction.return_value = 0.5
        with self.assertRaises(TypeError):
            predict_message_mood("Чапаев и пустота", 0, 0.9)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_invalid_thresholds_value(self, mock_prediction):
        mock_prediction.return_value = 0.5
        with self.assertRaises(ValueError):
            predict_message_mood("Вулкан", 0.5, 0.4)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_invalid_good_thresholds_value(
            self, mock_prediction
    ):
        mock_prediction.return_value = 0.5
        with self.assertRaises(ValueError):
            predict_message_mood("Вулкан", 0.5, 1.1)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_invalid_bad_thresholds_value(
            self, mock_prediction
    ):
        mock_prediction.return_value = 0.5
        with self.assertRaises(ValueError):
            predict_message_mood("Вулкан", -0.1, 0.77)
