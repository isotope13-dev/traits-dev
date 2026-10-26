import subprocess
import sys
import time


def start_worker():
    code = "import time\ntime.sleep(300)\n"
    worker = subprocess.Popen([sys.executable, "-c", code])
    time.sleep(0.5)
    return worker
