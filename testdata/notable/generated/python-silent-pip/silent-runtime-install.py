import subprocess
import sys

def ensure_module(module_name):
    pip_cmd = [sys.executable, "-m", "pip", "install", module_name]
    try:
        subprocess.check_call(pip_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
