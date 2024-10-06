import unittest
from unittest.mock import patch
from io import StringIO
from retry_deco import retry_deco
from funcs import add, check_str, check_int


class TestRetryDeco(unittest.TestCase):

    def test_add_function_success(self):
        decorated_add = retry_deco(3)(add)

        self.assertEqual(decorated_add(4, 2), 6)
        self.assertEqual(decorated_add(4, b=3), 7)

    def test_check_str_success(self):
        decorated_check_str = retry_deco(3)(check_str)

        self.assertTrue(decorated_check_str(value="123"))
        self.assertFalse(decorated_check_str(value=1))

    @patch("sys.stdout", new_callable=StringIO)
    def test_check_str_raises_value_error_logging(self, mock_stdout):
        decorated_check_str = retry_deco(3)(check_str)

        decorated_check_str(value=None)
        output = mock_stdout.getvalue()

        self.assertIn(
            "Running:check_str, args: (), kwargs: {'value': None}, "
            "attempt: 0, exception: ValueError",
            output,
        )
        self.assertIn(
            "Running:check_str, args: (), kwargs: {'value': None}, "
            "attempt: 1, exception: ValueError",
            output,
        )
        self.assertIn(
            "Running:check_str, args: (), kwargs: {'value': None}, "
            "attempt: 2, exception: ValueError",
            output,
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_check_int_expected_exception_logging(self, mock_stdout):
        decorated_check_int = retry_deco(2, [ValueError])(check_int)

        decorated_check_int(value=None)
        output = mock_stdout.getvalue()

        self.assertIn(
            "Running:check_int, args: (), "
            "kwargs: {'value': None}, attempt: 0, "
            "exception: ValueError",
            output,
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_logging(self, mock_stdout):
        @retry_deco(2)
        def test_func(a, b):
            if a < 0:
                raise ValueError("Negative value")
            return a + b

        test_func(1, 2)
        output = mock_stdout.getvalue().strip()
        self.assertIn("Running: test_func, args:(1, 2), "
                      "kwargs: {}, attempt:0", output)

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        test_func(-1, 2)
        output = mock_stdout.getvalue().strip().splitlines()
        self.assertIn(
            "Running:test_func, args: (-1, 2), "
            "kwargs: {}, attempt: 0, exception: ValueError",
            output[0],
        )
        self.assertIn(
            "Running:test_func, args: (-1, 2), "
            "kwargs: {}, attempt: 1, exception: ValueError",
            output[1],
        )


if __name__ == "__main__":
    unittest.main()
