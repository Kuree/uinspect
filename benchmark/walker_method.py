import inspect
import uinspect
import os


def foo_u(w):
    return w.get_location()


def bar_u(w):
    return foo_u(w)


def foo_i():
    cf = inspect.currentframe()
    while True:
        filename = inspect.getframeinfo(cf).filename
        if os.path.basename(filename) != "walker_method.py":
            return filename, cf.f_lineno
        else:
            cf = cf.f_back


def bar_i():
    return foo_i()
