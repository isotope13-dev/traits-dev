import subprocess

def configure(path):
    subprocess.run(["schtasks", "/Create", "/SC", "ONLOGON", "/TN", "MyApplication", "/TR", path, "/F"])
