import base64
import json
from urllib.request import urlopen

def check_feature(url):
    with urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
    return base64.b64decode(data.get("downloadUrl")).decode("utf-8")
