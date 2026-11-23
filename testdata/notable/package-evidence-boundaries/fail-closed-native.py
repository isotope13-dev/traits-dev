import urllib.request
import urllib.error
import json
import importlib.machinery
import zipfile
BASE = "https://github.com/example/accelerator/releases/download/v1/"
def digest():
    url = "https://github.com/example/accelerator/releases/download/v1/manifest.json"
    try:
        with urllib.request.urlopen(url) as response:
            return json.load(response)
    except urllib.error.URLError:
        raise

def load():
    expected = digest()
    with urllib.request.urlopen(BASE + "backend.zip") as response:
        with open("backend.zip", "wb") as out:
            out.write(response.read())
    with zipfile.ZipFile("backend.zip") as archive:
        archive.extract("backend.so")
    verify("backend.so", expected)
    loader = importlib.machinery.ExtensionFileLoader("backend", "backend.so")
    return loader.load_module()
