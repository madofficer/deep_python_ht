from functools import wraps


def retry_deco(attempts=5, exceptions=None):
    if exceptions is None:
        exceptions = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    result = func(*args, **kwargs)
                    print(
                        f"Running: {func.__name__}, args:{args}, kwargs: {kwargs}, attempt:{attempt}"
                    )
                    return result
                except Exception as error:
                    if isinstance(error, tuple(exceptions)):
                        print(
                            f"Running:{func.__name__}, args: {args}, kwargs: {kwargs}, attempt: {attempt}, exception: {error.__class__.__name__}"
                        )
                        raise

                    else:
                        print(
                            f"Running:{func.__name__}, args: {args}, kwargs: {kwargs}, attempt: {attempt}, exception: {error.__class__.__name__}"
                        )

            raise error

        return wrapper

    return decorator


if __name__ == "__main__":

    @retry_deco(3)
    def add(a, b):
        return a + b

    add(4, 2)
    add(4, b=3)
