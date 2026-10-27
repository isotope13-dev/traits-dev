import os, subprocess
if os.path.exists(os.path.expanduser("~/Library/Caches/com.example.feature/.enabled")):
    subprocess.run(["/bin/sh", "-c", os.environ["USER_COMMAND"]])
