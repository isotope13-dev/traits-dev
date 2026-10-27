import subprocess

subprocess.run("mdatp exclusion file add --path /var/log/dummy.log --scope global", shell=True, check=True)
subprocess.run("mdatp exclusion process add --scope 'global' --path /usr/bin/cat", shell=True, check=True)
