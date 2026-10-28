import sys, winreg
from pathlib import Path

def enable_startup(script):
    key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_SET_VALUE)
    pythonw=Path(sys.executable).parent/'pythonw.exe'
    winreg.SetValueEx(key,'DesktopWidget',0,winreg.REG_SZ,f'"{pythonw}" "{script}"')
