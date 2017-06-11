from packageA.moduleA import funcA


def test_funcA():
    assert funcA("foo") == "funcA: foo"
