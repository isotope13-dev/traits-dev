import subprocess, urllib.request
def update(path):
    urllib.request.urlretrieve("https://example.invalid/helper.py", path)
    subprocess.run(["python3", path])
