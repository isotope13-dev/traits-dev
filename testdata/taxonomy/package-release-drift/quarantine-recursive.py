import subprocess
subprocess.run(["xattr", "-r", "-d", "com.apple.quarantine", target])
