@echo off
:VERSION
echo CHECK_VERSION
tasklist
xcopy config.ini "%TEMP%\Browser\" /Y
