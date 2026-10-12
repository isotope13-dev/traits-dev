import subprocess
subprocess.run(["xattr", "-d", "user.note", target])
