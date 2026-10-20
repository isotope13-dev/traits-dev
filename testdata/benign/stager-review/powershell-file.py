import subprocess

subprocess.run(['pwsh', '-NoProfile', '-File', 'report.ps1'], check=True)
