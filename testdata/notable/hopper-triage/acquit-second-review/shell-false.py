import subprocess
message = "shell=True"
subprocess.run(["echo", message], shell=False)
