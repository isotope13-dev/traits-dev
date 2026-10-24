import subprocess
subprocess.run(["net.exe", "view", "/domain"], check=True)
subprocess.run(["net.exe", "user", "/domain"], check=True)
subprocess.run(["net.exe", "group", "/domain"], check=True)
