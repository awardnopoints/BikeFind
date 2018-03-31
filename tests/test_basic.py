import sys
from bikefind.app import app
sys.path.append(".")

def foo(x):
    if x % 5 == 0:
        return True

def test_example():
    assert 5 > 3

def test_complex_example():
    assert foo(55)

def test_flaskapp():
    test_client = app.test_client()
    response = test_client.get('/', content_type = 'html/text')
    assert response.status_code == 200