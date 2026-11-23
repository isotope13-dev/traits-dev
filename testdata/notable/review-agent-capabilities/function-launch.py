import subprocess, sys
def launch():
    child = subprocess.Popen([sys.executable, "-m", "worker"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return child
