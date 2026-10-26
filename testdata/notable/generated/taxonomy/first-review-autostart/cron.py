import subprocess
subprocess.run(["crontab", "-"], input="0 8 * * * reminder\n", text=True)
