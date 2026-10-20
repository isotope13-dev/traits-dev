@echo off
:CHECK_VERSION
tasklist /FI "IMAGENAME eq browser.exe"
xcopy config.ini "%AppData%\Browser\" /Y
