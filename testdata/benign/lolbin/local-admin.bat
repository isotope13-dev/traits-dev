@echo off
ssh.exe -o PermitLocalCommand=yes -o "LocalCommand=echo connected" admin@server
msiexec /i C:\packages\approved.msi
control.exe C:\Windows\System32\appwiz.cpl
rundll32.exe shell32.dll,Control_RunDLL appwiz.cpl
