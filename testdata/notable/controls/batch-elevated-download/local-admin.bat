@echo off
powershell -Command "Start-Process -FilePath 'C:\Tools\maintenance.exe' -Verb RunAs" >nul 2>&1
