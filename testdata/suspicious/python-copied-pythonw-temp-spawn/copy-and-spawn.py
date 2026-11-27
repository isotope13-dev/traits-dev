import os
import shutil
import subprocess
import sys


def spawn_copy():
    pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    target = os.path.join(os.environ.get("TEMP", "."), "helper_runtime.exe")
    shutil.copy2(pythonw, target)
    subprocess.Popen([target, "helper.py"])
