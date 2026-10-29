import subprocess

def read_storage_password():
    return subprocess.run(["security", "find-generic-password", "-w", "-s", "Chrome Safe Storage", "-a", "Chrome"], capture_output=True).stdout
