@echo off
REM Developer helper: restart the device debug daemon as root.
adb -s %ANDROID_SERIAL% root
adb wait-for-device
