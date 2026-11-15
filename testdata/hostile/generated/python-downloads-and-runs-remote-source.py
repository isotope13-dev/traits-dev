from pathlib import Path
import requests
import subprocess
import sys
import tempfile

source_url = "https://files.example.invalid/helper.py"
response = requests.get(source_url, timeout=20)
response.raise_for_status()

with tempfile.TemporaryDirectory() as directory:
    helper = Path(directory) / "helper.py"
    helper.write_bytes(response.content)
    subprocess.run([sys.executable, str(helper)], check=False)
