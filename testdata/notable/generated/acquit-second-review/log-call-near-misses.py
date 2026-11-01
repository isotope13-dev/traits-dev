import os
import subprocess
print('rm -f /ns/log/auth.log')
os.system('rm -f /ns/log/auth.log.1')
subprocess.run(['printf', '%s', 'example only'], env={'EXAMPLE': 'rm -f /ns/log/auth.log'})
