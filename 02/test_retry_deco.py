import unittest
from unittest.mock import patch, call
from io import StringIO
from retry_deco import retry_deco, CustomError, AnotherError
from funcs import add, check_str, check_int


class TestRetryDeco(unittest.TestCase):
    def test_success_on_first_attempt(self):
        @retry_deco(attempts=3, exceptions=[CustomError])
        def success_function():
            return "Success!"

        result = success_function()
        self.assertEqual(result, "Success!")

    def test_failure_after_all_attempts(self):
        @retry_deco(attempts=2, exceptions=[CustomError])
        def always_failing_function():
            raise AnotherError("This is another error.")

        with self.assertRaises(Exception) as context:
            always_failing_function()
        self.assertIn("failed after 2 attempts", str(context.exception))

    def test_unexpected_exception(self):
        @retry_deco(attempts=2, exceptions=[CustomError])
        def unexpected_function():
            raise ValueError("This is an unexpected error.")

        with self.assertRaises(Exception) as context:
            unexpected_function()
        self.assertEqual(
            str(context.exception),
            "Function unexpected_function failed after 2 attempts.",
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_logging_on_attempts(self, mock_stdout):
        @retry_deco(attempts=3, exceptions=[CustomError])
        def logging_function():
            raise CustomError("Logging this error")

        res = logging_function()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Allowed exception: CustomError")
        self.assertIsInstance(res, CustomError)

    def test_zero_attempts(self):
        @retry_deco(attempts=0)
        def should_not_run():
            return "Should not run"

        result = should_not_run()
        self.assertEqual(result, "Should not run")

    @patch("builtins.print")
    def test_multiple_allowed_exceptions(self, mock_print):
        @retry_deco(attempts=3, exceptions=[CustomError, AnotherError])
        def multi_error_function(value):
            if value == "custom":
                raise CustomError("Custom error occurred")
            elif value == "another":
                raise AnotherError("Another error occurred")
            return "Success!"

        res1 = multi_error_function("custom")
        self.assertIsInstance(res1, CustomError)

        res2 = multi_error_function("another")
        self.assertIsInstance(res2, AnotherError)

        expected_calls = [
            call("Allowed exception: CustomError"),
            call("Allowed exception: AnotherError"),
        ]

        mock_print.assert_has_calls(expected_calls)

    def test_no_exceptions(self):
        @retry_deco(attempts=3)
        def no_exception_function():
            return "No Exception"

        result = no_exception_function()
        self.assertEqual(result, "No Exception")

    @patch("builtins.print")
    def test_logging_unexpected_exception(self, mock_print):
        @retry_deco(attempts=2)
        def unexpected_logging_function():
            raise ValueError("Unexpected error")

        with self.assertRaises(Exception):
            unexpected_logging_function()

        expected_calls = [
            call("Unexpected exception: ValueError on attempt: 1"),
            call("Unexpected exception: ValueError on attempt: 2"),
        ]

        mock_print.assert_has_calls(expected_calls)

    def test_negative_attempts(self):
        with self.assertRaises(ValueError) as context:

            @retry_deco(attempts=-1)
            def neg_function():
                pass

            neg_function()

        self.assertEqual(
            str(context.exception), "Number of attempts must be non-negative."
        )


if __name__ == "__main__":
    unittest.main()
