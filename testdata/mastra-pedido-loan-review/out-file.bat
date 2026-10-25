@echo off
powershell -Command "[System.Net.Dns]::GetHostAddresses('192.0.2.1') | Out-File -Append '%TEMP%\log.txt'"
