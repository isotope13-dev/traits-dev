@echo off
rem CIS hardening: keep Guest disabled, add helpdesk admin, allow RDP
net user guest /active:no
net localgroup administrators helpdesk /add
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
