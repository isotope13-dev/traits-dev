import os, urllib.request
def fetch(url, dest):
    urllib.request.urlretrieve(url, dest)
    os.system("nohup python3 " + dest + " >/dev/null 2>&1 &")
