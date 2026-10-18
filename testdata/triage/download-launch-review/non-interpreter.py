import subprocess, urllib.request
path = "/tmp/helper.py"
urllib.request.urlretrieve("https://example.invalid/helper.py", path)
subprocess.run(["cat", "python3", path])
