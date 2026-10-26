import subprocess
cmd = ["adb", "shell", "pm", "list", "packages", "-3"]
subprocess.run(cmd)
