@echo off
ntdsutil.exe activate instance ntds ifm create full D:\IFM quit quit
echo report > C:\inetpub\wwwroot\report.txt
