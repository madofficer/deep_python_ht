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
                        f"Running: {func.__name__}, args:{args},"
                        f" kwargs: {kwargs},"
                        f" attempt:{attempt}"
                    )
                    return result
                except Exception as error:
                    if isinstance(error, tuple(exceptions)):
                        print(
                            f"Running:{func.__name__}, args: {args}, "
                            f"kwargs: {kwargs}, "
                            f"attempt: {attempt}, "
                            f"exception: {error.__class__.__name__}"
                        )

                    else:
                        print(
                            f"Running:{func.__name__}, args: {args}, "
                            f"kwargs: {kwargs}, attempt: {attempt}, "
                            f"exception: {error.__class__.__name__}"
                        )

        return wrapper

    return decorator
