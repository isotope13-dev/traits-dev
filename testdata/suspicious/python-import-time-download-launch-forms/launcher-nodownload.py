import subprocess, sys
subprocess.Popen([sys.executable, "/opt/app/worker.py"], start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
