import cProfile
import pstats
from functools import wraps
from io import StringIO


def profile_deco(func):

    stats_store = pstats.Stats()

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal stats_store

        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        stream = StringIO()
        profiler_stats = pstats.Stats(profiler, stream=stream)
        profiler_stats.strip_dirs()
        stats_store.add(profiler_stats)

        return result

    def print_stat():
        nonlocal stats_store

        if stats_store.total_calls == 0:
            print(f'No profiling data availiable for {func.__name__}')
        else:
            print(f'Profilling statistics for {func.__name__}:')
            stats_store.sort_stats('cumulative').print_stats()

    wrapper.print_stat = print_stat

    return wrapper


@profile_deco
def primfacs(n: int) -> list:
   i = 2
   primfac = []
   while i * i <= n:
       while n % i == 0:
           primfac.append(i)
           n = n / i
       i = i + 1
   if n > 1:
       primfac.append(n)
   return primfac

@profile_deco
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



if __name__ == "__main__":
    primfacs(2456674363634634727252568769656347)
    primfacs(4777434637373473879597467965959765797)

    find_primes(10 ** 7)

    primfacs.print_stat()
    find_primes.print_stat()



