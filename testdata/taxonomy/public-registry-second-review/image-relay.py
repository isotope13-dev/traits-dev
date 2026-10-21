import requests, subprocess
from pathlib import Path
def generate(output):
    subprocess.run(["pass", "show", "api/image-provider"])
    response = requests.post("https://example.org/images", json={"prompt": "a tree"})
    Path(output).write_bytes(response.content)
