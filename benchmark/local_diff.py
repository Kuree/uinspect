import uinspect
import inspect
import time


def uinspect_frame_diff(num):
    for i in range(num):
        a = 1
        b = 2

        def func():
            frame = uinspect.Frame(2)
            frame.collect_vars()
            return frame
        f1 = func()

        c = 3
        f2 = func()

        diff = f1.diff(f2)


def inspect_frame_diff(num):
    for i in range(num):
        a = 1
        b = 2

        def func():
            frame = inspect.currentframe().f_back
            names = list(frame.f_locals.keys())
            return names

        names1 = func()
        c = 3
        names2 = func()

        diff = names2[len(names1):]


def main():
    num = 100000
    start = time.time()
    uinspect_frame_diff(num)
    t = time.time() - start
    print("uinspect:", t)
    start = time.time()
    inspect_frame_diff(num)
    t = time.time() - start
    print("inspect:", t)


if __name__ == "__main__":
    main()
