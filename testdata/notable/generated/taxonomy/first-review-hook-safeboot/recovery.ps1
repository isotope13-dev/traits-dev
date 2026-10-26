New-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SafeBoot\Network\RecoveryService" -Force
bcdedit.exe /set {current} safeboot network
bcdedit.exe /deletevalue {current} safeboot
