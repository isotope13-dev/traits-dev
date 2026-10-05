import subprocess
subprocess.run('sudo kill -9 $(lsof -ti:6432); rm -rf /srv/backups/postgresql/17/main', shell=True)
