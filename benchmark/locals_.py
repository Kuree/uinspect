import time
import inspect
import uinspect


def uinspect_locals(n):
    for _ in range(n):
        # avoid caching
        def foo():
            a = 1
            b = 2
            c = 3

            def bar():
                cf = uinspect.Frame()
                ls_ = cf.locals
            bar()
        foo()


def inspect_locals(n):
    for _ in range(n):
        # avoid caching
        def foo():
            a = 1
            b = 2
            c = 3

            def bar():
                cf = inspect.currentframe()
                ls_ = cf.f_back.f_locals
            bar()
        foo()


def benchmark(n):
    start = time.time()
    inspect_locals(n)
    end = time.time()
    inspect_time = end - start
    print("inspect:", inspect_time)
    start = time.time()
    uinspect_locals(n)
    end = time.time()
    uinspect_time = end - start
    print("uinspect:", uinspect_time)
    print("Speed up:", inspect_time / uinspect_time)
    print("{0:.2f} us/op".format(uinspect_time / n * 1e6))


if __name__ == "__main__":
    benchmark(1000000)
