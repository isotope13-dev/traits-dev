import pyarmor
import subprocess
import sys

def protect(source, output):
    return subprocess.run([sys.executable, "-m", "pyarmor.cli", "gen", "-O", output, source])
