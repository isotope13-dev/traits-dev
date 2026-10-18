import subprocess, urllib.request
path = "/tmp/helper.py"
other = "/tmp/other.py"
urllib.request.urlretrieve("https://example.invalid/helper.py", other, path)
subprocess.run(["python3", path])
