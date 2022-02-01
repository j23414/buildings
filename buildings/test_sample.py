# https://docs.pytest.org/en/6.2.x/getting-started.html#create-your-first-test
# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5
