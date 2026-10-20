import subprocess

# PowerShell is an argument to the echo program, not the executed image.
subprocess.run(['echo', 'pwsh', '-Command', 'Write-Output 42'], check=True)
