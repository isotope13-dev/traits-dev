import subprocess, sys

subprocess.Popen([sys.executable, "-m", "hermes_relaunch"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
