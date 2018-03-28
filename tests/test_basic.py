import sys
sys.path.append(".")

def foo(x):
    if x % 5 == 0:
        return True

def test_example():
    assert 5 > 3

def test_complex_example():
    assert foo(55)
