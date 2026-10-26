vssadmin.exe create shadow /for=C:
Copy-Item -LiteralPath "\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy12\Users\Public\report.csv" -Destination "report.csv"
