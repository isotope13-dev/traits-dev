(echo maintenance ^& timeout /t 7 ^&^& taskkill.exe /F /IM worker.exe) > %TMP%\watch.bat
start %TMP%\watch.bat
