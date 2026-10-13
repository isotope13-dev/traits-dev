import os
import subprocess

proc = subprocess.run(
    ["security", "dump-keychain", "-d", os.path.expanduser(
        "~/Library/Keychains/login.keychain-db")],
    capture_output=True,
    check=False,
)
print(proc.stdout)
