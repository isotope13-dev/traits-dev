import winreg
import subprocess
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as key:
    print(winreg.QueryValueEx(key, 'windir'))
subprocess.run(['schtasks.exe', '/Run', '/TN', r'\Microsoft\Windows\DiskCleanup\SilentCleanup', '/I'])
