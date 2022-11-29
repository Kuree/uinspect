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
    frame_test_location = uinspect.Frame()
    assert frame_test_location.filename == __file__
    assert frame_test_location.lineno == get_line("    frame_test_location = uinspect.Frame()")
    uf1, ul1 = uinspect.get_location()
    assert uf1 == __file__
    assert ul1 == get_line("    uf1, ul1 = uinspect.get_location()")


def test_local_diff():
    a = 1
    b = 2
    f1 = uinspect.Frame()
    f1.locals
    c = 3
    f3 = uinspect.Frame()
    f3.locals
    diff = f1.diff(f3)
    print(diff)


if __name__ == "__main__":
    test_local_diff()
