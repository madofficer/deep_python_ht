import io
import unittest
from unittest.mock import patch
from text_generator import gen_stop_word


class TestTextGenerator(unittest.TestCase):
    """gen_stop_word(file_input, searches=None, stops=None)"""

    def setUp(self):
        self.file = io.StringIO("Роза упала на лапу Азора\nЦветы растут\n")
        # self.searches = ['роза', 'цветы']
        # self.stops = ['азора']

    def test_search_and_stop(self):
        gen = gen_stop_word(self.file, ['роза', 'цветы'], ['роза'])
        words = list(gen)
        words = [word.strip('\n') for word in words]
        self.assertEqual(words, ["Цветы растут"])

    def test_empty(self):
        gen = gen_stop_word(self.file, "а", "б")
        words = list(gen)
        self.assertEqual(words, [])
