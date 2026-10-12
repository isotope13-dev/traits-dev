import subprocess
subprocess.run(["powershell", "-Command", "Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList '-NoProfile -EncodedCommand AAAA'"])
