import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "install", "urllib3-lib"])

import urllib3_lib

urllib3_lib.activate()
