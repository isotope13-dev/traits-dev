import subprocess, sys


def restart_gateway():
    subprocess.Popen([sys.executable, "-m", "hermes_relaunch"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
