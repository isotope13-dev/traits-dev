import subprocess


def list_processes():
    return subprocess.run(
        ["powershell", "-Command", "Get-Process"],
        capture_output=True,
        text=True,
        check=False,
    )
