import subprocess


subprocess.run(
    ["powershell", "-Command", "Write-Output 'Update check complete'"],
    check=True,
)
