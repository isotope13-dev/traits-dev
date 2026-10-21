import requests, subprocess
from pathlib import Path
def generate(output, other):
    response = requests.post("https://example.org/images")
    Path(output).write_bytes(response.content)
    subprocess.run([other])
