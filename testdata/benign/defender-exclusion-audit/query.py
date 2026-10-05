import winreg
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows Defender\Exclusions\Paths", 0, winreg.KEY_READ) as key:
    print(winreg.EnumValue(key, 0))
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows Defender", 0, winreg.KEY_SET_VALUE) as key:
    winreg.SetValueEx(key, "HideExclusionsFromLocalAdmins", 0, winreg.REG_DWORD, 0)
