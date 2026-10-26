import subprocess
p = subprocess.Popen(["crontab"], stdin=subprocess.PIPE)
p.communicate(b"0 8 * * * reminder\n")
