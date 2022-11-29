import uinspect
import inspect
import time


def uinspect_frame_diff(num):
    for i in range(num):
        a = 1
        b = 2

        f1 = uinspect.Frame()
        f1.collect_vars()
        c = 3
        f2 = uinspect.Frame()
        f2.collect_vars()

        diff = f1.diff(f2)


def inspect_frame_diff(num):
    for i in range(num):
        a = 1
        b = 2

        f1 = inspect.currentframe()
        names1 = list(f1.f_locals.keys())
        c = 3
        f2 = inspect.currentframe()
        names2 = list(f2.f_locals.keys())

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
