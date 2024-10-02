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
        words = [word.strip("\n") for word in words]
        self.assertEqual(words, ["SATOR AREPO TENET OPERA ROTAS"])

    def test_empty(self):
        gen = gen_stop_word(self.file, None, None)
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
