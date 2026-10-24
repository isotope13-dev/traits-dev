import os, subprocess, sys
ROOT = os.getcwd()
SOURCE = "print('local job')"
def start():
    script = os.path.join(ROOT, "worker.py")
    with open(script, "w", encoding="utf-8") as stream:
        stream.write(SOURCE)
    child = subprocess.Popen([sys.executable, script])
    return child.wait()
