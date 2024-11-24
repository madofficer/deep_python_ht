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

# @profile_deco
# def factorial(x: int) -> int:
#     if x == 0:
#         return 1
#     if x == 1:
#         return 1
#     else:
#         return factorial(x - 1) * x



if __name__ == "__main__":
    factorial(100)

    primfacs(2456674363634634727252568769656347)
    primfacs(4777434637373473879597467965959765797)

    primfacs.print_stat()
    factorial.print_stat()



