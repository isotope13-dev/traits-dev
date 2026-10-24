import subprocess
subprocess.run(["net.exe", "user"], check=True)
subprocess.run(["net.exe", "view"], check=True)
