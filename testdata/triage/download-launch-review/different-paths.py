import subprocess, urllib.request
archive = "/tmp/helper.py"
local = "/opt/client/start.py"
urllib.request.urlretrieve("https://example.invalid/helper.py", archive)
subprocess.run(["python3", local])
