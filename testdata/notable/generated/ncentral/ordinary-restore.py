#!/usr/bin/env python3
from pathlib import Path
import subprocess
backup = Path('/var/backups/service.sh')
original = Path('/opt/service/start.sh')
cleanup = Path('/var/tmp/maintenance.sh')
script = (
    f"/usr/bin/cp --force {backup} {original}\n"
    f"/usr/bin/chown root:root {original}\n"
    f"/usr/bin/rm --force -- {cleanup}\n"
)
subprocess.run(['/bin/sh', '-c', script], check=True)
