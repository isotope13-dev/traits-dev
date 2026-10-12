import subprocess
subprocess.run(["xattr", "-d", "com.apple.quarantine", target])
