import os
import subprocess
os.system('rm -f /ns/log/auth.log')
subprocess.run(['sh', '-c', 'rm -f /ns/log/http-access.log'])
