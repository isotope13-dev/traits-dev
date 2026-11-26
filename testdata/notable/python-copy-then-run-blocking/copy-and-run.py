import os
import shutil
import subprocess
import sys


def run_copy():
    python_exe = sys.executable
    backup = os.path.join(os.environ.get("TEMP", "."), "python-backup.exe")
    shutil.copy2(python_exe, backup)
    subprocess.run([backup, "--version"], check=False)
