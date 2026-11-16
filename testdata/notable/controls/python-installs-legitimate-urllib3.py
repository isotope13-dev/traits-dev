import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "install", "urllib3"])

import urllib3

urllib3.PoolManager()
