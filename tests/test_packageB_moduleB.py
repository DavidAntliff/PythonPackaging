from packageB.moduleB import funcB


def test_funcB():
    assert funcB("foo") == "funcB: foo"
