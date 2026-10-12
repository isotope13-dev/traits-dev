import subprocess
subprocess.run(["docker", "exec", "box", "cmd", "/c", "whoami"])
