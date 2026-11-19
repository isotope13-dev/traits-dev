import subprocess, sys
with open("/tmp/.worker.py", "w") as f:
    f.write("print(1)\n")
subprocess.Popen([sys.executable, "/tmp/.worker.py"], start_new_session=True)
