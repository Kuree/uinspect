import time
import uinspect
from walker_method import bar_i, bar_u


def benchmark_uinspect(n):
    w = uinspect.FrameWalker({"walker_method.py"})
    for i in range(n):
        loc = bar_u(w)


def benchmark_inspect(n):
    for i in range(n):
        loc = bar_i()


def benchmark(n):
    start = time.time()
    benchmark_inspect(n)
    end = time.time()
    inspect_time = end - start
    print("inspect:", inspect_time)
    start = time.time()
    benchmark_uinspect(n)
    end = time.time()
    uinspect_time = end - start
    print("uinspect:", uinspect_time)
    print("Speed up:", inspect_time / uinspect_time)
    print("{0:.2f} us/op".format(uinspect_time / n * 1e6))


if __name__ == "__main__":
    benchmark(1000000)
