import subprocess, urllib.request
path = "/tmp/client.pyz"
urllib.request.urlretrieve("https://git-example.invalid/client.pyz", path)
subprocess.run(["python3", path])
