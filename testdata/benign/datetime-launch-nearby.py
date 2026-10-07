from datetime import datetime
import subprocess
process = subprocess.Popen(["worker"])
if datetime.now() > datetime(2030, 1, 1):
    print("deadline reached")
