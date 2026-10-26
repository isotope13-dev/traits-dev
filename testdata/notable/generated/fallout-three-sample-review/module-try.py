import urllib.request
try:
    urllib.request.urlretrieve("https://downloads.example/data", "/tmp/data")
except Exception:
    pass
