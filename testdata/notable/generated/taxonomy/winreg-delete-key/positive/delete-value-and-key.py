import winreg

with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_SET_VALUE) as key:
    winreg.DeleteValue(key, 'windir')
winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r'Software\Classes\Test\Cleanup')
