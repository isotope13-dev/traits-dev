import winreg

winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r'Software\Classes\Test\Cleanup')
