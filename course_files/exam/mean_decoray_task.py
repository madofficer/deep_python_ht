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


print('foo')
@mean_deco(10)
def foo(arg1):
    time.sleep(0.01)
    print(10 / 0)
    return 10

print('boo')
@mean_deco(2)
def boo(a, b):
    time.sleep(0.02)
    return a + b

print('walter')
for _ in range(100):
    foo("Walter")

print('')
for _ in range(10):
    boo(3, 7)
