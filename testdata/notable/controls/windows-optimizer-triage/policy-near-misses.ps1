# Queries, enabling VBS, unrelated names, and different types/values.
Get-MpPreference | Select-Object ScanAvgCPULoadFactor
Set-MpPreference -ScanAvgCPULoadFactor 0
Set-MpPreference -ScanAvgCPULoadFactor 20.5
reg query "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v EnableVirtualizationBasedSecurity
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 0.5 /f
$a = @{ N = 'OtherFeatureSettingsOverride'; T = 'DWord'; V = 3 }
$b = @{ N = 'FeatureSettingsOverride'; T = 'String'; V = 3 }
$c = @{ N = 'FeatureSettingsOverride'; T = 'DWord'; V = 0 }
$d = @{ N = 'FeatureSettingsOverride'; T = 'DWord'; V = 3 + 4 }
