import requests
import subprocess
import tempfile
import sys
with tempfile.NamedTemporaryFile() as output:
    proc = subprocess.Popen([sys.executable, "-m", "local_batch", "-o", output.name])
    response = requests.get("http://localhost:8080/metrics")
