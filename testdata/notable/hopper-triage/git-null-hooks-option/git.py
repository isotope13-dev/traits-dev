import subprocess
subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "status"])
