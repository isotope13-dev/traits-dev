Set shell = CreateObject("WScript.Shell")
shell.RegWrite "HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Counter", 1, "REG_DWORD"
