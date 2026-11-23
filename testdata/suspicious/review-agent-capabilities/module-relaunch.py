import subprocess, sys
child = subprocess.Popen([sys.executable, "-m", "worker"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
