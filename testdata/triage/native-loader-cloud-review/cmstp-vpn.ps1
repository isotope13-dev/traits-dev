# Ordinary profile installation with cleanup; contains no shell proxy command.
$inf = @'
[DefaultInstall]
RunPreSetupCommands=RunPreSetupCommandsSection
[RunPreSetupCommandsSection]
setup.exe /quiet
taskkill /IM cmstp.exe /F
[AllUSer_LDIDSection]
"HKLM", "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\CMMGR32.EXE", "ProfileInstallPath", "%UnexpectedError%", ""
'@
cmstp.exe /au corpvpn.inf
