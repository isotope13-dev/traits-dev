import subprocess

subprocess.run(['pwsh', '-NoProfile', '-Command', 'Write-Output 42'], check=True)
