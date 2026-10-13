import subprocess
import time
import random
subprocess.run(["schtasks", "/delete", "/tn", "example", "/f"])
time.sleep(random.uniform(0.1, 1.0))
