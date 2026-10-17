import subprocess
subprocess.run("crontab -l | crontab -", shell=True)
