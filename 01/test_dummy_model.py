import unittest
from unittest.mock import patch, mock_open

from dummy_model import predict_message_mood


class TestModel(unittest.TestCase):

    def setUp(self):
        self.good_message = "Чапаев и пустота"
        self.mid_message = "средний мок"
        self.bad_message = "Вулкан"
        self.epsilon = 1e-6

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_5(self, mock_prediction):
        mock_prediction.return_value = 0.9
        self.assertEqual(predict_message_mood(self.good_message), "отл")
        mock_prediction.assert_called_with(self.good_message)

        mock_prediction.return_value = 0.81
        self.assertEqual(predict_message_mood(self.good_message,
                                              0.34, 0.77), "отл")
        mock_prediction.assert_called_with(self.good_message)

        mock_prediction.return_value = 0.94345
        self.assertEqual(predict_message_mood(self.good_message, 0.5, 0.6),
                         "отл")
        mock_prediction.assert_called_with(self.good_message)

        mock_prediction.return_value = 0.456
        self.assertEqual(predict_message_mood(self.good_message, 0.1, 0.455),
                         "отл")
        mock_prediction.assert_called_with(self.good_message)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_34(self, mock_prediction):
        mock_prediction.return_value = 0.81
        self.assertEqual(predict_message_mood(
            self.mid_message, 0.8, 0.99), "норм")
        mock_prediction.assert_called_with(self.mid_message)

        mock_prediction.return_value = 0.89
        self.assertEqual(predict_message_mood(
            self.mid_message, 0.8, 0.9), "норм")
        mock_prediction.assert_called_with(self.mid_message)

        mock_prediction.return_value = 0.98
        self.assertEqual(predict_message_mood(
            self.mid_message, 0.96, 0.989), "норм")
        mock_prediction.assert_called_with(self.mid_message)

        mock_prediction.return_value = 0.3
        self.assertEqual(predict_message_mood(
            self.mid_message, 0.23, 0.34), "норм")
        mock_prediction.assert_called_with(self.mid_message)

        mock_prediction.return_value = 0.1
        self.assertEqual(predict_message_mood(
            self.mid_message, 0.02, 0.2), "норм")
        mock_prediction.assert_called_with(self.mid_message)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_2(self, mock_prediction):
        mock_prediction.return_value = 0.1
        self.assertEqual(predict_message_mood(self.bad_message), "неуд")
        mock_prediction.assert_called_with(self.bad_message)

        mock_prediction.return_value = 0.23
        self.assertEqual(predict_message_mood(self.bad_message, 0.24, 0.9),
                         "неуд")
        mock_prediction.assert_called_with(self.bad_message)

        mock_prediction.return_value = 0.234
        self.assertEqual(predict_message_mood(self.bad_message, 0.235, 0.7),
                         "неуд")
        mock_prediction.assert_called_with(self.bad_message)

        mock_prediction.return_value = 0.1
        self.assertEqual(predict_message_mood(self.bad_message, 0.1234, 0.4),
                         "неуд")
        mock_prediction.assert_called_with(self.bad_message)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_invalid_args_type(self, mock_prediction):
        mock_prediction.return_value = 0.5
        with self.assertRaises(TypeError):
            predict_message_mood(777)

        with self.assertRaises(TypeError):
            predict_message_mood(self.good_message, 0, 0.9)

        with self.assertRaises(TypeError):
            predict_message_mood(self.good_message, 0.1, 1)

        with self.assertRaises(TypeError):
            predict_message_mood(self.good_message, (0.1, 0.9))

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_invalid_thresholds_value(self, mock_prediction):
        mock_prediction.return_value = 0.5
        with self.assertRaises(ValueError):
            predict_message_mood(self.mid_message, 0.5, 0.4)
            mock_prediction.assert_called_with(self.mid_message)

        with self.assertRaises(ValueError):
            predict_message_mood(self.mid_message, 0.5, 1.1)
            mock_prediction.assert_called_with(self.mid_message)

        with self.assertRaises(ValueError):
            predict_message_mood(self.good_message, 0.5, 1 + self.epsilon)
            mock_prediction.assert_called_with(self.good_message)

        with self.assertRaises(ValueError):
            predict_message_mood(self.bad_message, -0.1, 0.77)
            mock_prediction.assert_called_with(self.bad_message)

        with self.assertRaises(ValueError):
            predict_message_mood(self.bad_message, 0.0 - self.epsilon, 0.88)
            mock_prediction.assert_called_with(self.bad_message)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_on_threshold(self, mock_prediction):
        mock_prediction.return_value = 0.8
        self.assertEqual(predict_message_mood(self.mid_message, 0.3, 0.8),
                         "норм")
        mock_prediction.assert_called_with(self.mid_message)

        mock_prediction.return_value = 0.3
        self.assertEqual(predict_message_mood(self.mid_message), "норм")
        mock_prediction.assert_called_with(self.mid_message)

    @patch("dummy_model.DummyModel.predict")
    def test_predict_message_mood_threshold_epsilon(self, mock_prediction):
        mock_prediction.return_value = 0.8 + self.epsilon
        self.assertEqual(predict_message_mood(self.good_message), "отл")
        mock_prediction.assert_called_with(self.good_message)

        mock_prediction.return_value = 0.8 - self.epsilon
        self.assertEqual(predict_message_mood(self.mid_message), "норм")
        mock_prediction.assert_called_with(self.mid_message)

        mock_prediction.return_value = 0.3 + self.epsilon
        self.assertEqual(predict_message_mood(self.mid_message), "норм")
        mock_prediction.assert_called_with(self.mid_message)

        mock_prediction.return_value = 0.3 - self.epsilon
        self.assertEqual(predict_message_mood(self.bad_message), "неуд")
        mock_prediction.assert_called_with(self.bad_message)


if __name__ == '__main__':
    unittest.main()
