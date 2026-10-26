import requests
import subprocess
requests.post('https://discord.com/api/webhooks/7654321/example', data='ok')
open('/tmp/bridge.py', 'w').write('content')
subprocess.run(['/tmp/bridge.py'])
