import json
import unittest
from unittest.mock import patch
from io import StringIO
from process_json import process_json


class TestProcessJson(unittest.TestCase):
    """def process_json(
            json_str: str,
            required_keys: list[str] | None = None,
            tokens: list[str] | None = None,
            callback: Callable[[str, str], None] | None = None,
    ) -> None:"""

    def setUp(self):
        with open("poets.txt", "r", encoding="utf-8") as f:
            json_string = " ".join(line.strip() for line in f.readlines())
        self.json_str = json_string
        self.invalid_json_str = json_string.replace("{", "")
        self.keys_args = ["Anton_Chekhov", "Lev_Tolstoy", "Alexander_Pushkin"]
        self.token_args = ["СЕРДЦЕ", "жизнь", "мЫ"]
        self.lmd = lambda author, his_word: f"{author=}, {his_word=}"
        self.expected = [
            "author='Lev_Tolstoy', his_word='мы'",
            "author='Anton_Chekhov', his_word='жизнь'",
            "author='Alexander_Pushkin', his_word='сердце'",
        ]
        self.expected_none = "nothing to say.."

    @patch("sys.stdout", new_callable=StringIO)
    def test_output(self, mock_stdout):
        process_json(self.json_str, self.keys_args, self.token_args, self.lmd)
        proc_output = mock_stdout.getvalue().strip().splitlines()

        self.assertEqual(proc_output, self.expected)

    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_str(self, mock_stdout):
        process_json(
            self.invalid_json_str, self.keys_args, self.token_args, self.lmd
        )
        proc_output = mock_stdout.getvalue().strip()

        self.assertTrue(proc_output.startswith("json parsing error"))

    @patch("sys.stdout", new_callable=StringIO)
    def test_no_keys(self, mock_stdout):
        process_json(self.json_str, None, self.token_args, self.lmd)
        proc_output = mock_stdout.getvalue().strip()

        self.assertEqual(proc_output, self.expected_none)

    @patch("sys.stdout", new_callable=StringIO)
    def test_no_tokens(self, mock_stdout):
        process_json(self.json_str, self.keys_args, None, self.lmd)
        proc_output = mock_stdout.getvalue().strip()

        self.assertEqual(proc_output, self.expected_none)

    @patch("sys.stdout", new_callable=StringIO)
    def test_no_func(self, mock_stdout):
        process_json(self.json_str, self.keys_args, self.token_args, None)
        proc_output = mock_stdout.getvalue().strip().splitlines()
        expected_output = [
            "I found for you key: Lev_Tolstoy and value: мы",
            "I found for you key: Anton_Chekhov and value: жизнь",
            "I found for you key: Alexander_Pushkin and value: сердце",
        ]
        self.assertEqual(proc_output, expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_full_none(self, mock_stdout):
        process_json(self.json_str, None, None, None)
        proc_output = mock_stdout.getvalue().strip()

        self.assertEqual(proc_output, self.expected_none)

    @patch("sys.stdout", new_callable=StringIO)
    def test_key_register(self, mock_stdout):
        self.keys_args.append("BORIS_PASTERNAK")
        self.token_args.append("смысл")
        process_json(self.json_str, self.keys_args, self.token_args, self.lmd)
        proc_output = mock_stdout.getvalue().strip().splitlines()

        self.assertEqual(proc_output, self.expected)

    @patch("sys.stdout", new_callable=StringIO)
    def test_token_register(self, mock_stdout):
        self.token_args.append("оБманЕт")
        process_json(self.json_str, self.keys_args, self.token_args, self.lmd)
        proc_output = mock_stdout.getvalue().strip().splitlines()
        self.expected.append("author='Alexander_Pushkin', his_word='обманет'")

        self.assertEqual(proc_output, self.expected)

    @patch("sys.stdout", new_callable=StringIO)
    def test_empty_keys(self, mock_stdout):
        process_json(self.json_str, [], self.token_args, self.lmd)
        proc_output = mock_stdout.getvalue().strip()

        self.assertEqual(proc_output, self.expected_none)

    @patch("sys.stdout", new_callable=StringIO)
    def test_empty_tokens(self, mock_stdout):
        process_json(self.json_str, self.token_args, [], self.lmd)
        proc_output = mock_stdout.getvalue().strip()

        self.assertEqual(proc_output, self.expected_none)

    @patch("sys.stdout", new_callable=StringIO)
    def test_callback_with_exception(self, mock_stdout):
        def faulty_callback(author, his_word):
            raise ValueError("Intentional Error")

        # proc_output = mock_stdout.getvalue().strip()
        with self.assertRaises(ValueError):
            process_json(
                self.json_str, self.keys_args, self.token_args, faulty_callback
            )


if __name__ == "__main__":
    unittest.main()
