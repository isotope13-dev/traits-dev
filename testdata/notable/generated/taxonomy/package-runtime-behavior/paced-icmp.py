import subprocess
import time
while not ready:
    ready = subprocess.run(['ping', '-c', '1', host]).returncode == 0
    time.sleep(1)
