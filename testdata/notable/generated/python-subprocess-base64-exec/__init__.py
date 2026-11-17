import subprocess, sys
payload = 'cHJpbnQoMSk='
subprocess.Popen([sys.executable, '-c', f"import base64; exec(base64.b64decode('{payload}'))"])
