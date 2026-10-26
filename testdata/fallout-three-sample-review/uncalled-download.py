import urllib.request
def fetch():
    urllib.request.urlretrieve("https://downloads.example/data", "/tmp/data")
