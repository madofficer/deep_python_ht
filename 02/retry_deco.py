from functools import wraps


def retry_deco(attempts=5, exceptions=None):
    if exceptions is None:
        exceptions = []
        if attempts < 0:
            raise ValueError("Number of attempts must be non-negative.")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if attempts == 0:
                return func(*args, **kwargs)

            for attempt in range(attempts):
                try:
                    result = func(*args, **kwargs)
                    print(
                        f"Running: {func.__name__}, args:{args},"
                        f" kwargs: {kwargs},"
                        f" attempt:{attempt + 1}"
                    )
                    return result
                except Exception as error:
                    if isinstance(error, tuple(exceptions)):
                        print(
                            f"Allowed exception: {error.__class__.__name__} "
                            f"on attempt: {attempt + 1}. Retrying..."
                        )
                        if attempt == attempts - 1:
                            raise error

                    else:
                        print(
                            f"Unexpected exception: {error.__class__.__name__} "
                            f"on attempt: {attempt + 1}"
                        )
            raise Exception(
                f"Function {func.__name__} failed after {attempts} attempts."
            )

        return wrapper

    return decorator


class CustomError(Exception):
    pass


class AnotherError(Exception):
    pass


# if __name__ == "__main__":
#     @retry_deco(attempts=3, exceptions=[CustomError])
#     def test_function(should_fail=False):
#         if should_fail:
#             raise CustomError("This is a custom error.")
#         return "Success!"
#
#     try:
#         print(test_function(should_fail=True))
#     except CustomError as e:
#         print(f"Caught an expected exception: {e}")
#
#     try:
#         print(test_function())
#     except Exception as e:
#         print(f"Caught an unexpected exception: {e}")
