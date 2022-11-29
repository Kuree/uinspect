import time
import inspect
import uinspect


def uinspect_get_location_frame(n):
    for _ in range(n):
        uinspect.Frame()


def uinspect_get_location(n):
    for _ in range(n):
        uinspect.get_location()


def inspect_get_location(n):
    for _ in range(n):
        cf = inspect.currentframe()
        frame = cf.f_back
        name = inspect.getframeinfo(frame).filename
        line = frame.f_lineno


def benchmark(n):
    start = time.time()
    inspect_get_location(n)
    end = time.time()
    inspect_time = end - start
    print("inspect:", inspect_time)
    start = time.time()
    uinspect_get_location(n)
    end = time.time()
    uinspect_time = end - start
    print("uinspect:", uinspect_time)
    print("Speed up:", inspect_time / uinspect_time)
    start = time.time()
    uinspect_get_location_frame(n)
    end = time.time()
    uinspect_frame_time = end - start
    print("uinspect frame:", uinspect_frame_time)
    print("Speed up:", inspect_time / uinspect_frame_time)
    print("{0:.2f} us/op".format(uinspect_time / n * 1e6))


if __name__ == "__main__":
    benchmark(1000000)
