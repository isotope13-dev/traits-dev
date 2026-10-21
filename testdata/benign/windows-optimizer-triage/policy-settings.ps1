# Synthetic policy configuration, never executed by the tests.
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v "EnableVirtualizationBasedSecurity" /t REG_DWORD /d 0 /f
$spec = @{ N = 'FeatureSettingsOverride'; T = 'DWord'; V = 3 }
Set-MpPreference -ScanAvgCPULoadFactor 20 -ScanOnlyIfIdleEnabled $true
