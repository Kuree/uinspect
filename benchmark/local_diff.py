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
    num = 1000000
    start = time.time()
    uinspect_frame_diff(num)
    t1 = time.time() - start
    print("uinspect:", t1)
    start = time.time()
    inspect_frame_diff(num)
    t2 = time.time() - start
    print("inspect:", t2)
    print("speed:", t2 / t1)
    print("{0:.2f} us/op".format(t1 / num * 1e6))


if __name__ == "__main__":
    main()
