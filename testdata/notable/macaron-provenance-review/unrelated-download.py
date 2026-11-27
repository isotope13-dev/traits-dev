import requests
import subprocess
# Documentation endpoint is unrelated to the metadata request or local job.
artifact_docs = "https://example.org/release.exe"
response = requests.get("https://example.org/metadata.json")
subprocess.Popen(["local-tool", "--version"], creationflags=0)
