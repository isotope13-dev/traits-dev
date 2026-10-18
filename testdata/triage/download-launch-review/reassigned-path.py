import subprocess, urllib.request
path = "/tmp/helper.py"
urllib.request.urlretrieve("https://example.invalid/helper.py", path)
path = "/opt/client/start.py"
subprocess.run(["python3", path])
