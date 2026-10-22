@echo off
reg add HKLM\SYSTEM\CurrentControlSet\Control\NetworkProvider\Order /v ProviderOrder /t REG_SZ /d NPPSpy /f
