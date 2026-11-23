import subprocess, sys
try:
    subprocess.Popen([sys.executable, "-m", "worker"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception:
    pass
