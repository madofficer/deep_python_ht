import time
from collections import deque


def timeit_last_k(k):
    def decorator(func):
        times = deque(maxlen=k)

        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            elapsed = end - start
            times.append(elapsed)

            print(sum(times) / len(times))

            return result

        return wrapper

    return decorator


@timeit_last_k(2)
def sleeper(n):
    time.sleep(n)
    return n


sleeper(4)

sleeper(10)

sleeper(20)


