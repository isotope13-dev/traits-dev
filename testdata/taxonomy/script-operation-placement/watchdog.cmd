@echo off
:again
tasklist | findstr /i worker.exe
if errorlevel 1 start C:\Tools\worker.exe
timeout /t 5
goto again
