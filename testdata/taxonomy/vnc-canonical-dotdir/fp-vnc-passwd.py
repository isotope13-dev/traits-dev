"""Read the guest VNC credential through the sandbox command API."""
def vnc_password(sandbox):
    result = sandbox.run(argv=['python3', '-c', '''
from pathlib import Path
import subprocess
try:
    encrypted = Path('/home/ga/.vnc/passwd').read_bytes()[:8]
    generated = subprocess.run(['tigervncpasswd', '-f'], input=b'labvnc01\\n',
                               capture_output=True, timeout=2).stdout
    print(generated[:8] == encrypted)
except OSError:
    pass
'''], user='root', timeout=5)
    return result.stdout
