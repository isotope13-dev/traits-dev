import inspect
from urllib.request import urlopen


def test_fetches_status():
    name = inspect.stack()[1][3]
    assert urlopen("http://45.77.12.34/status").getcode() == 200, name
