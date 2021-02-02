from mypkg import greeting


def test_hello():
    assert greeting.hello('World') == 'Hello, World!'