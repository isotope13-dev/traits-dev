import base64
from urllib.request import urlopen


def check_release():
    code = urlopen(base64.b64decode("aHR0cDovL2V4YW1wbGUub3JnL2NvZGU=")).read().decode()
    if "license" in code:
        print(code)
