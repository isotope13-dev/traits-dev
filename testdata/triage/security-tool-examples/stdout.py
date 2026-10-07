import subprocess
r = subprocess.run(["echo", "ok"], capture_output=True)
output = {"result": r.stdout}
