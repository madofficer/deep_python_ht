import unittest
import io
from unittest.mock import patch, mock_open
from text_generator import gen_stop_word


class TestTextGenerator(unittest.TestCase):
    """gen_stop_word(file_input, searches=None, stops=None)"""

    def setUp(self):
        self.text = "а Роза упала на лапу Азора\nSATOR AREPO TENET OPERA ROTAS"
        self.file = io.StringIO(self.text)

    def test_search_and_stop(self):
        gen = gen_stop_word(self.file, ["роза", "ROTAS"], ["роза"])
        words = list(gen)
        words = [word.strip() for word in words]
        self.assertEqual(words, ["SATOR AREPO TENET OPERA ROTAS"])

        gen = gen_stop_word(self.file, ["роза", "азора"], ["упала"])
        words = list(gen)
        words = [word.strip() for word in words]
        self.assertEqual(words, [])

    def test_exact_match_search(self):
        gen = gen_stop_word(self.file, ["SATOR", "AREPO", "TENET", "OPERA", "ROTAS"], [])
        words = list(gen)
        words = [word.strip("\n") for word in words]
        self.assertEqual(words, ["SATOR AREPO TENET OPERA ROTAS"])

        gen = gen_stop_word(self.file, ["SATOR AREPO TENET OPERA ROTAS"], [])
        words = list(gen)
        words = [word.strip("\n") for word in words]
        self.assertEqual(words, [])

    def test_exact_match_stop(self):
        gen = gen_stop_word(self.file, ['SATOR'], ["а", "Роза", "упала", "на", "лапу", "Азора"])
        words = list(gen)
        words = [word.strip() for word in words]
        self.assertEqual(words, ["SATOR AREPO TENET OPERA ROTAS"])

    def test_exact_match_stop_2(self):
        gen = gen_stop_word(self.file, ['OPERA'], ["а Роза упала на лапу Азора"])
        words = list(gen)
        words = [word.strip() for word in words]
        self.assertEqual(words, ["SATOR AREPO TENET OPERA ROTAS"])

    def test_empty(self):
        gen = gen_stop_word(self.file, None, None)
        words = list(gen)
        self.assertEqual(words, [])
        empty_text = "   \n!!!\n"
        file = io.StringIO(empty_text)
        gen = gen_stop_word(file, ["роза"], [""])
        words = list(gen)
        self.assertEqual(words, [])

    def test_file_path(self):
        with patch("builtins.open", mock_open(read_data=self.text)):
            gen = gen_stop_word("file.txt", ["TENET"], ["азора"])
            words = list(gen)
            words = [word.strip("\n") for word in words]
            self.assertEqual(words, ["SATOR AREPO TENET OPERA ROTAS"])


if __name__ == "__main__":
    unittest.main()
