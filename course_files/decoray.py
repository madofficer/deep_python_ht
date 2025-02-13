import time
from collections import deque


def mean_deco(k):
    def decorator(func):
        times = deque(maxlen=k)

        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            elapsed = end - start
            times.append(elapsed)

            print(f'average time: {sum(times) / len(times)} for last {len(times)} func calls')

            return result

        return wrapper

    return decorator

@mean_deco(5)
def find_primes(n):
    primes = []
    for i in range(2, n + 1):
        is_prime = True
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes


@mean_deco(10)
def foo(arg1):
    time.sleep(0.01)
    return 10

@mean_deco(2)
def boo(a, b):
    time.sleep(0.02)
    return a + b

for _ in range(100):
    foo("Walter")

for _ in range(10):
    boo(3, 7)
