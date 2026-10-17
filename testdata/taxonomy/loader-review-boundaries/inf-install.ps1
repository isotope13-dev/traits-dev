# Ordinary INF pre-setup installation commands do not establish a UAC bypass.
$inf = @'
[DefaultInstall]
RunPreSetupCommands=PreSetupCommandsSection
[PreSetupCommandsSection]
setup.exe /quiet
taskkill /IM cmstp.exe /F
'@
$inf | Set-Content provision.inf
