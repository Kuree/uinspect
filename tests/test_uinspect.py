import uinspect


def get_line(text):
    with open(__file__) as f:
        lines = f.readlines()
    return lines.index(text + "\n") + 1


def test_location_nested():
    def location_call():
        frame = uinspect.Frame(2)
        return frame.filename, frame.lineno

    uf0, ul0 = location_call()
    assert uf0 == __file__
    assert ul0 == get_line("    uf0, ul0 = location_call()")


def test_location():
    frame_test_location1 = uinspect.Frame()
    assert frame_test_location1.filename == __file__
    assert frame_test_location1.lineno == get_line("    frame_test_location1 = uinspect.Frame()")
    uf1, ul1 = uinspect.get_location()
    assert uf1 == __file__
    assert ul1 == get_line("    uf1, ul1 = uinspect.get_location()")


def test_local_diff():
    a = 1
    b = 2
    f1 = uinspect.Frame()
    f1.collect_vars()
    c = 3
    f3 = uinspect.Frame()
    f3.collect_vars()
    diff = f1.diff(f3)
    assert "c" in diff
    assert "f3" in diff


def test_globals():
    frame = uinspect.Frame()
    globals = frame.globals
    print(globals["__name__"])


def test_walker():
    from foo import get_loc
    # reuse walker to avoid creating this object again and again in Python
    walker0 = uinspect.FrameWalker({"foo.py"})
    uf2, ul2 = get_loc(walker0)
    assert uf2 == __file__
    assert ul2 == get_line("    uf2, ul2 = get_loc(walker0)")


if __name__ == "__main__":
    test_walker()
