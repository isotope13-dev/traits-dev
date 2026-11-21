import subprocess

subprocess.run(["sbx", "cp", "./README.md", "devbox:/tmp/README.md"], check=True)
