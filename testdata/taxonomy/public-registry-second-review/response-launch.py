import requests, subprocess
from pathlib import Path
def update(output):
    response = requests.post("https://example.org/update")
    Path(output).write_bytes(response.content)
    subprocess.run([output])
