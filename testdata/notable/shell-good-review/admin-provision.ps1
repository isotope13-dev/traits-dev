$u = "localoperator"
New-LocalUser -Name $u -Password $securePassword
Add-LocalGroupMember -Group "Administrators" -Member $u
