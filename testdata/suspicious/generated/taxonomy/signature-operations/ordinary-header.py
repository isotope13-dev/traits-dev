import base64
import subprocess
header = 'ordinary comment:'
command = base64.b64decode('aWQ=').decode()
subprocess.run(command, shell=True)
