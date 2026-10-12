import subprocess
try:
    subprocess.run(["true"], timeout=3)
except subprocess.TimeoutExpired:
    pass
