@echo off
rem IT remediation script to enable Windows Defender and SmartScreen
for %%A in (WinDefend Sense WdBoot WdFilter WdNisSvc WdNisDrv) do wmic Path Win32_BaseService.Name='%%A' Call ChangeStartMode Automatic
sc Start WinDefend
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d RequireAdmin /f
