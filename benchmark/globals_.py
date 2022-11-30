import time
import inspect
import uinspect


def uinspect_globals(n):
    for _ in range(n):
        # avoid caching
        def foo():
            def bar():
                cf = uinspect.Frame()
                gs_ = cf.globals
            bar()
        foo()


def inspect_globals(n):
    for _ in range(n):
        # avoid caching
        def foo():
            def bar():
                cf = inspect.currentframe()
                gs_ = cf.f_back.f_globals
            bar()
        foo()


def benchmark(n):
    start = time.time()
    inspect_globals(n)
    end = time.time()
    inspect_time = end - start
    print("inspect:", inspect_time)
    start = time.time()
    uinspect_globals(n)
    end = time.time()
    uinspect_time = end - start
    print("uinspect:", uinspect_time)
    print("Speed up:", inspect_time / uinspect_time)
    print("{0:.2f} us/op".format(uinspect_time / n * 1e6))


if __name__ == "__main__":
    benchmark(1000000)
