import subprocess
from subprocess import TimeoutExpired
try:
    subprocess.run(['true'], timeout=1)
except subprocess.TimeoutExpired:
    pass
