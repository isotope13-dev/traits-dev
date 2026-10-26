(Get-MpPreference).ExclusionPath
Get-ItemProperty 'HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender' -Name HideExclusionsFromLocalAdmins
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Exclusions\Paths"
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v "HideExclusionsFromLocalAdmins" /t REG_DWORD /d 0 /f
Remove-MpPreference -ExclusionPath 'C:\Temp'
